from datetime import datetime
from pandas import DataFrame
from numpy import nan

from rest_framework.response import Response
from rest_framework import status

from universities.models import ConsumerUnit
from contracts.models import Contract
from tariffs.models import Tariff
from tariffs.serializers import BlueTariffSerializer, GreenTariffSerializer

from mec_energia.settings import MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION

from recommendation.calculator import ContractRecommendationResult

HEADERS_FOR_CONSUMPTION_HISTORY = [
    'date', 'peak_consumption_in_kwh', 'off_peak_consumption_in_kwh',
    'peak_measured_demand_in_kw', 'off_peak_measured_demand_in_kw',
]

def _generate_tariffs_as_table(blue_tariff: Tariff, green_tariff: Tariff):
    serialized_blue = BlueTariffSerializer(blue_tariff).data
    serialized_green = GreenTariffSerializer(green_tariff).data
    # ????? serialized_green['missing_field_in_green'] = None

    tariff_labels = {*serialized_blue, *serialized_green}

    tariffs_table: list[dict] = []
    for label in tariff_labels:
        row = {'label': label}
        row['blue'] = serialized_blue[label] if label in serialized_blue else None
        row['green'] = serialized_green[label] if label in serialized_green else None
        tariffs_table.append(row)

    return tariffs_table

def _generate_plot_demands_in_current_contract(consumption_history: DataFrame, contract_peak_demand_in_kw: int, contract_off_peak_demand_in_kw: int):
    '''A coluna `contract_demand_in_kw` tá sendo criada com `history_len`
    valores pra ficar fácil pro Frontend só plotar essa curva de
    `contract_demand_in_kw`.'''

    history_len = len(consumption_history)
    current_contract_demands: DataFrame = consumption_history[[
        'date', 'peak_measured_demand_in_kw', 'off_peak_measured_demand_in_kw']]\
        .astype({'peak_measured_demand_in_kw': int, 'off_peak_measured_demand_in_kw': int}, errors='ignore')
    current_contract_demands.insert(0, 'contract_peak_demand_in_kw', [contract_peak_demand_in_kw]*history_len)
    current_contract_demands.insert(0, 'contract_off_peak_demand_in_kw', [contract_off_peak_demand_in_kw]*history_len)
    current_contract_demands_dict = current_contract_demands.to_dict('list')
    return current_contract_demands_dict

def _generate_plot_demands_costs_in_current_contract(current_contract_recommendation: DataFrame):
    current_contract_demands_costs: DataFrame = current_contract_recommendation[
        ['date', 'consumption_cost_in_reais', 'demand_cost_in_reais']]
    return current_contract_demands_costs.to_dict('list')

def _generate_plot_demand_and_consumption_costs_in_current_contract(current_contract_recommendation: DataFrame):
    current_demand_and_consumption_costs: DataFrame = current_contract_recommendation[[
        'date', 'consumption_cost_in_reais', 'demand_cost_in_reais']]
    return current_demand_and_consumption_costs.to_dict('list')

def _generate_plot_recommended_contract_demands(
    consumption_history: DataFrame,
    recommendation_frame: DataFrame
):
    '''Comparação entre as demandas medidas e a demanda de contrato
    recomendada'''

    demands: DataFrame = recommendation_frame[[
        'date', 'peak_demand_in_kw', 'off_peak_demand_in_kw']]\
        .astype({'peak_demand_in_kw': int, 'off_peak_demand_in_kw': int}, errors='ignore')
    demands.insert(1, 'peak_measured_demand_in_kw', consumption_history.peak_measured_demand_in_kw)
    demands.insert(1, 'off_peak_measured_demand_in_kw', consumption_history.off_peak_measured_demand_in_kw)
    return demands.to_dict('list')

def _generate_plot_demand_and_consumption_costs_in_recommended_contract(recommendation_frame: DataFrame):
    demand_and_consumption_costs: DataFrame = recommendation_frame[[
        'date', 'consumption_cost_in_reais', 'demand_cost_in_reais']]
    return demand_and_consumption_costs.to_dict('list')

def _generate_plot_current_vs_estimated_costs(recommendation: ContractRecommendationResult):
    result = DataFrame()
    result.insert(0, 'total_cost_in_reais_in_recommended', recommendation.frame.contract_cost_in_reais)
    result.insert(0, 'total_cost_in_reais_in_current', recommendation.current_contract.cost_in_reais)
    result.insert(0, 'date', recommendation.frame.date)

    result.replace({nan: None}, inplace=True)
    result_dict = result.to_dict('list')
    result_dict['total_total_cost_in_reais_in_current'] = recommendation.current_contract.cost_in_reais.sum()
    result_dict['total_total_cost_in_reais_in_recommended'] = recommendation.frame.contract_cost_in_reais.sum()
    return result_dict

def _generate_table_current_vs_recommended_contracts(recommendation: ContractRecommendationResult):
    result = DataFrame()
    result.insert(0, 'absolute_difference', recommendation.frame.absolute_difference)

    result.insert(0, 'consumption_cost_in_reais_in_recommended', recommendation.frame.consumption_cost_in_reais)
    result.insert(0, 'demand_cost_in_reais_in_recommended', recommendation.frame.demand_cost_in_reais)
    result.insert(0, 'total_cost_in_reais_in_recommended', recommendation.frame.contract_cost_in_reais)

    result.insert(0, 'consumption_cost_in_reais_in_current', recommendation.current_contract.consumption_cost_in_reais)
    result.insert(0, 'demand_cost_in_reais_in_current', recommendation.current_contract.demand_cost_in_reais)
    result.insert(0, 'total_cost_in_reais_in_current', recommendation.current_contract.cost_in_reais)

    result.insert(0, 'date', recommendation.frame.date)

    current_vs_recommended_contracts_totals: dict[str, float] = {
        'absolute_difference': result.absolute_difference.sum(),
        'consumption_cost_in_reais_in_recommended': result.consumption_cost_in_reais_in_recommended.sum(),
        'demand_cost_in_reais_in_recommended': result.demand_cost_in_reais_in_recommended.sum(),
        'total_cost_in_reais_in_recommended': result.total_cost_in_reais_in_recommended.sum(),
        'consumption_cost_in_reais_in_current': result.consumption_cost_in_reais_in_current.sum(),
        'demand_cost_in_reais_in_current': result.demand_cost_in_reais_in_current.sum(),
        'total_cost_in_reais_in_current': result.total_cost_in_reais_in_current.sum(),
    }

    result.replace({nan: None}, inplace=True)
    return (result.to_dict('records'), current_vs_recommended_contracts_totals)

def build_response(
    recommendation: ContractRecommendationResult,
    consumption_history: DataFrame,
    contract: Contract,
    consumer_unit: ConsumerUnit,
    blue: Tariff,
    green: Tariff,
    errors: list[str],
    energy_bills_count: int,
    ):
    '''Reponsável por APENAS construir o objeto `Response` de endpoint'''
    # FIXME: um pouquinho de gambiarra
    if recommendation == None:
        current_demands = _generate_plot_demands_in_current_contract(
            consumption_history,
            int(contract.peak_contracted_demand_in_kw),
            int(contract.off_peak_contracted_demand_in_kw))

        return Response({
            'errors': errors,
            'current_contract': {
                'university': consumer_unit.university.name,
                'distributor': contract.distributor.name,
                'consumer_unit': consumer_unit.name,
                'consumer_unit_code': consumer_unit.code,
                'supply_voltage': contract.supply_voltage,
                'tariff_flag': contract.tariff_flag,
                'subgroup': contract.subgroup,
                'peak_contracted_demand_in_kw': contract.peak_contracted_demand_in_kw,
                'off_peak_contracted_demand_in_kw': contract.off_peak_contracted_demand_in_kw,
            },
            'plot_consumption_history': consumption_history[HEADERS_FOR_CONSUMPTION_HISTORY 
              + ['contract_peak_demand_in_kw', 'contract_off_peak_demand_in_kw']].to_dict('list'),
        })

    current_demands = _generate_plot_demands_in_current_contract(
        consumption_history,
        int(contract.peak_contracted_demand_in_kw),
        int(contract.off_peak_contracted_demand_in_kw))
    # current_demands_costs = _generate_plot_demands_costs_in_current_contract(recommendation.current_contract)
    current_demand_and_consumption_costs = _generate_plot_demand_and_consumption_costs_in_current_contract(recommendation.current_contract)

    recommended_demands = _generate_plot_recommended_contract_demands(consumption_history, recommendation.frame)
    demands_and_consumption_costs_in_recommended_contract = _generate_plot_demand_and_consumption_costs_in_recommended_contract(recommendation.frame)
    current_vs_estimated_costs = _generate_plot_current_vs_estimated_costs(recommendation)
    current_vs_recommended_contract, totals = _generate_table_current_vs_recommended_contracts(recommendation)
    table_tariffs = _generate_tariffs_as_table(blue, green)

    costs_percentage_difference = totals['absolute_difference'] / totals['total_cost_in_reais_in_current']

    return Response({
        'generated_on': datetime.now(),
        'current_contract': {
            'university': consumer_unit.university.name,
            'distributor': contract.distributor.name,
            'consumer_unit': consumer_unit.name,
            'consumer_unit_code': consumer_unit.code,
            'supply_voltage': contract.supply_voltage,
            'tariff_flag': contract.tariff_flag,
            'subgroup': contract.subgroup,
            'peak_contracted_demand_in_kw': contract.peak_contracted_demand_in_kw,
            'off_peak_contracted_demand_in_kw': contract.off_peak_contracted_demand_in_kw,
        },
        'table_tariffs': table_tariffs,
        'table_consumption_history': consumption_history[HEADERS_FOR_CONSUMPTION_HISTORY].to_dict('records'),
        'plot_consumption_history': consumption_history[HEADERS_FOR_CONSUMPTION_HISTORY 
          + ['contract_peak_demand_in_kw', 'contract_off_peak_demand_in_kw']].to_dict('list'),
        'plot_current_contract_demands': current_demands,
        # 'plot_current_contract_demands_costs': current_demands_costs,
        'plot_current_contract_demand_and_consumption_costs': current_demand_and_consumption_costs,
        'recommended_contract': {
            'university': consumer_unit.university.name,
            'distributor': contract.distributor.name,
            'consumer_unit': consumer_unit.name,
            'consumer_unit_code': consumer_unit.code,
            'supply_voltage': contract.supply_voltage,
            'subgroup': contract.subgroup,
            'tariff_flag': recommendation.tariff_flag,
            'off_peak_demand_in_kw': recommendation.off_peak_demand_in_kw,
            'peak_demand_in_kw': recommendation.peak_demand_in_kw,
        },
        'plot_recommended_demands': recommended_demands,
        'plot_recommended_demand_and_consumption_costs': demands_and_consumption_costs_in_recommended_contract,
        'plot_current_vs_estimated_costs': current_vs_estimated_costs,
        # Os dois campos seguintes devem fornecer dados suficientes para o
        # plot "Custo-base atual vs estimado" e para a tabela Custo-base (R$)
        'table_current_vs_recommended_contract': current_vs_recommended_contract,
        'table_current_vs_recommended_contract_totals': totals,
        'should_renew_contract': costs_percentage_difference > MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION,
        'energy_bills_count': energy_bills_count,
        'costs_percentage_difference': round(costs_percentage_difference, 3),
        'errors': errors,
    })

