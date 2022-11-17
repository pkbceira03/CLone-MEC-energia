import json
import pytest
from datetime import date
from rest_framework import status
from rest_framework.test import APIClient

from users.models import UniversityUser
from universities.models import University, ConsumerUnit
from contracts.models import Contract, EnergyBill

ENDPOINT = '/api/consumer-units/'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin@admin.com'

@pytest.mark.django_db
class TestConsumerUnitsProperties:
    def test_reads_consumer_unit_properties_no_energy_bill_filled(self):
        response = self.client.get(f'{ENDPOINT}{self.consumer_unit_1.id}/')
        consumer_unit = json.loads(response.content)

        assert self.contract_1.start_date == consumer_unit['date']
        assert False == consumer_unit['is_current_energy_bill_filled']
        assert 12 == consumer_unit['pending_energy_bills_number']
        assert status.HTTP_200_OK == response.status_code

    # FIXME: Teste travando na primeira linha
    
    """ def test_reads_consumer_unit_properties_current_energy_bill_filled(self):
        response = self.client.get(f'{ENDPOINT}{self.consumer_unit_2.id}/')
        geted_consumer_unit = json.loads(response.content)

        assert geted_consumer_unit['date'] == self.contract_2.start_date
        assert geted_consumer_unit['is_current_energy_bill_filled'] == True
        assert geted_consumer_unit['pending_energy_bills_number'] == 5
        assert response.status_code == status.HTTP_200_OK """


    def setup_method(self):
        self.client = APIClient()
        self.date_now = date.today()
        university_dict = {
            'name': 'Universidade de Brasília',
            'cnpj': '00038174000143'
        }
        self.university = University(**university_dict)
        self.university.save()
        self.user = UniversityUser.objects.create_user(
            email=EMAIL, password=PASSWORD, university=self.university)
        self.client.login(email=EMAIL, password=PASSWORD)
        self.consumer_unit_1_dict = {
            'name': 'Darcy Ribeiro',
            'code': '000000000',
            'created_on': '2022-10-02',
            'is_active': True,
            'university': self.university
        }
        self.consumer_unit_1 = ConsumerUnit(**self.consumer_unit_1_dict)
        self.consumer_unit_1.save()
        self.consumer_unit_2_dict = {
            'name': 'Faculdade do Gama',
            'code': '111111111',
            'created_on': '2022-11-01',
            'is_active': True,
            'university': self.university
        }
        self.consumer_unit_2 = ConsumerUnit(**self.consumer_unit_2_dict)
        self.consumer_unit_2.save()
        self.contract_1_dict = {
            'start_date': '2022-01-01',
            'end_date': '2023-01-01',
            'tariff_flag': 'V',
            'sub_group': 'A1',
            'supply_voltage': 100.00,
            'peak_contracted_demand_in_kw': 100.00,
            'off_peak_contracted_demand_in_kw': 100.00,
            'consumer_unit': self.consumer_unit_1
        }
        self.contract_1 = Contract(**self.contract_1_dict)
        self.contract_1.save()
        self.contract_2_dict = {
            'start_date': f'2023-01-02',
            'end_date': '2024-01-02',
            'tariff_flag': 'A',
            'sub_group': 'A2',
            'supply_voltage': 200.00,
            'peak_contracted_demand_in_kw': 200.00,
            'off_peak_contracted_demand_in_kw': 200.00,
            'consumer_unit': self.consumer_unit_2
        }
        self.contract_2 = Contract(**self.contract_2_dict)
        self.contract_2.save()
        self.energy_bill_dict = {
            'date': f'{self.date_now}',
            'invoice_in_reais': 100.00,
            'is_atypical': False,
            'peak_consumption_in_kwh': 100.00,
            'off_peak_consumption_in_kwh': 100.00,
            'peak_measured_demand_in_kw': 100.00,
            'off_peak_measured_demand_in_kw': 100.00,
            'contract': self.contract_2,
            'consumer_unit': self.consumer_unit_2
        }
        self.energy_bill = EnergyBill(**self.energy_bill_dict)
        self.energy_bill.save()
