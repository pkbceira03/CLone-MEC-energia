from pandas import DataFrame

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema

from mec_energia.settings import MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION, IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION, MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_UPDATE
from universities.models import ConsumerUnit
from contracts.models import Contract
from tariffs.models import Tariff

from recommendation.calculator import RecommendationCalculator, CONSUMPTION_HISTORY_HEADERS
from recommendation.helpers import fill_with_pending_dates
from recommendation.response import build_response
from recommendation.serializers import RecommendationSettingsSerializerForDocs


HEADERS_FOR_CONSUMPTION_HISTORY = [
    'date', 'peak_consumption_in_kwh', 'off_peak_consumption_in_kwh',
    'peak_measured_demand_in_kw', 'off_peak_measured_demand_in_kw',
]

class RecommendationViewSet(ViewSet):
    http_method_names = ['get']

    def retrieve(self, request: Request, pk=None):
        '''Deve ser fornecido o ID da Unidade Consumidora.

        `plotRecommendedDemands`: se a tarifa recomendada é VERDE, os campos
        `plotRecommendedDemands.offPeakDemandInKw` e
        `plotRecommendedDemands.peakDemandInKw`
        possuem o mesmo valor. Você pode plotar os dois ou plotar apenas um
        desses campos como demanda única.

        `table_current_vs_recommended_contract.absolute_difference = current - recommended`
        '''

        consumer_unit_id = pk
        try:
            consumer_unit = ConsumerUnit.objects.get(pk=consumer_unit_id)
        except ConsumerUnit.DoesNotExist:
            return Response({'errors': [f'Consumer unit does not exist']}, status=status.HTTP_404_NOT_FOUND)

        contract = consumer_unit.current_contract
        distributor_id = contract.distributor.id

        blue, green = self._get_tariffs(contract.subgroup, distributor_id)
        consumption_history, pending_bills_dates = self._get_energy_bills_as_consumption_history(consumer_unit, contract)

        consumption_history_length = len(consumption_history)
        if consumption_history_length < MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION:
            return Response(
                {'errors': ['Not enough energy bills for recommendation.'
                f' Got {consumption_history_length} bills']},
                status=status.HTTP_400_BAD_REQUEST)

        calculator = RecommendationCalculator(
            consumption_history=consumption_history,
            current_tariff_flag=contract.tariff_flag,
            blue_tariff=blue.as_blue_tariff(),
            green_tariff=green.as_green_tariff(),
        )

        recommendation = calculator.calculate()
        fill_with_pending_dates(recommendation, consumption_history, pending_bills_dates)

        return build_response(
            HEADERS_FOR_CONSUMPTION_HISTORY,
            recommendation,
            consumption_history,
            contract,
            consumer_unit,
            blue,
            green,
        )

    def _get_energy_bills_as_consumption_history(self, consumer_unit: ConsumerUnit, contract: Contract):
        bills = consumer_unit.get_energy_bills_for_recommendation()
        pending_bills = consumer_unit.get_energy_bills_pending()
        bills_list: list[dict] = []
        for bill in bills:
            if bill['energy_bill'] == None:
                continue

            b = bill['energy_bill']
            bills_list.append({
                'date': b['date'],
                'peak_consumption_in_kwh': float(b['peak_consumption_in_kwh']),
                'off_peak_consumption_in_kwh': float(b['off_peak_consumption_in_kwh']),
                'peak_measured_demand_in_kw': float(b['peak_measured_demand_in_kw']),
                'off_peak_measured_demand_in_kw': float(b['off_peak_measured_demand_in_kw']),
                'contract_peak_demand_in_kw': float(contract.peak_contracted_demand_in_kw),
                'contract_off_peak_demand_in_kw': float(contract.off_peak_contracted_demand_in_kw),
                'peak_exceeded_in_kw': 0.0,
                'off_peak_exceeded_in_kw': 0.0,
            })

        bills_list.reverse()
        consumption_history = DataFrame(bills_list, columns=CONSUMPTION_HISTORY_HEADERS)
        pending_bills_dates = [f"{b['year']}-{b['month']}-01" for b in pending_bills]
        return (consumption_history, pending_bills_dates)

    def _get_tariffs(self, subgroup: str, distributor_id: int):
        tariffs = Tariff.objects.filter(subgroup=subgroup, distributor_id=distributor_id)
        tariffs_count = tariffs.count()
        assert 2 == tariffs_count, f'Got {tariffs_count} tariffs'
        blue_tariff = tariffs.filter(flag=Tariff.BLUE).first()
        green_tariff = tariffs.filter(flag=Tariff.GREEN).first()
        return (blue_tariff, green_tariff)

class RecommendationSettings(ViewSet):
    http_method_names = ['get']

    @swagger_auto_schema(responses={200: RecommendationSettingsSerializerForDocs()})
    def list(self, _):
        settings = {
            'MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION': MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION,
            'IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION': IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION,
            'MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_UPDATE': MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_UPDATE
        }
        return Response(settings)
