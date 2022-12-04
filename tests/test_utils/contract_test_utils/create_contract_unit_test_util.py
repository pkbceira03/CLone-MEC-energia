from datetime import date
from contracts.models import Contract

class CreateContractTestUtil:
    contract_dicts = [
        {
            'start_date': date(year = 2022, month = 1, day = 1),
            'tariff_flag': 'V',
            'supply_voltage': 100.00,
            'peak_contracted_demand_in_kw': 100.00,
            'off_peak_contracted_demand_in_kw': 100.00,
        },
        {
            'start_date': date(year=2023, month = 1, day = 1),
            'tariff_flag': 'A',
            'supply_voltage': 250.00,
            'peak_contracted_demand_in_kw': 250.00,
            'off_peak_contracted_demand_in_kw': 250.00,
        },
        {
            'start_date': date(year=2024, month = 1, day = 1),
            'tariff_flag': 'A',
            'supply_voltage': 69,
            'peak_contracted_demand_in_kw': 250.00,
            'off_peak_contracted_demand_in_kw': 250.00,
        },
        {
            'start_date': date(year=2025, month = 1, day = 1),
            'tariff_flag': 'V',
            'supply_voltage': 100.00,
            'peak_contracted_demand_in_kw': 100.00,
            'off_peak_contracted_demand_in_kw': 100.00,
        },
        {
            'start_date': date(year=2050, month = 1, day = 1),
            'tariff_flag': 'A',
            'supply_voltage': 70,
            'peak_contracted_demand_in_kw': 250.00,
            'off_peak_contracted_demand_in_kw': 250.00,
        },
        {
            'start_date': date(year=2023, month = 1, day = 1),
            'tariff_flag': 'V',
            'supply_voltage': 100.00,
            'peak_contracted_demand_in_kw': 100.00,
            'off_peak_contracted_demand_in_kw': 100.00,
        },
    ]
    
    def create_contract(index, consumer_unit, distributor) -> Contract:
        contract_dict = CreateContractTestUtil.get_contract_dict(index)
        
        contract = Contract.objects.create(
            distributor = distributor,
            consumer_unit = consumer_unit,
            start_date = contract_dict['start_date'],
            tariff_flag = contract_dict['tariff_flag'],
            supply_voltage = contract_dict['supply_voltage'],
            peak_contracted_demand_in_kw = contract_dict['peak_contracted_demand_in_kw'],
            off_peak_contracted_demand_in_kw = contract_dict['off_peak_contracted_demand_in_kw'],
        )

        return contract

    def get_contract_dict(index):
        return CreateContractTestUtil.contract_dicts[index]