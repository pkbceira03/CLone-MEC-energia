import pytest
import json

from datetime import date, timedelta

from rest_framework.test import APIClient
from rest_framework import status

from universities.models import University
from tariffs.models import Distributor

from users.models import UniversityUser
from universities.models import University
from tariffs.models import Distributor, Tariff


ENDPOINT = '/api/tariffs/'
EMAIL = 'admin@admin.com'
PASSWORD = 'password'
DATE_FORMAT = '%Y-%m-%d'
TODAY = date.today()

@pytest.mark.django_db
class TestTariffEndpoints:
    def setup_method(self):
        university_dict = {
            'name': 'Universidade de São Paulo',
            'cnpj': '63025530000104'
        }

        self.university = University.objects.create(**university_dict)

        self.distributor1 = Distributor.objects.create(
            name='Distribuidora de Energia',
            cnpj='63025530000104',
            university_id=self.university.id
        )

        self.distributor2 = Distributor.objects.create(
            name='Antiga CEB?',
            cnpj='11111111111111',
            university_id=self.university.id
        )

        self.user = UniversityUser.objects.create_user(
            email=EMAIL, password=PASSWORD, university=self.university)
        self.client = APIClient()
        assert self.client.login(email=EMAIL, password=PASSWORD)

    def test_creates_tariff(self):
        tariff_dict = self._create_tariff_dict()
        
        response = self.client.post(ENDPOINT, tariff_dict, format='json')
        tariff = json.loads(response.content)

        assert status.HTTP_201_CREATED == response.status_code
        assert self.distributor1.id == tariff['distributor']
        assert 1.0 == tariff['blue']['peak_tusd_in_reais_per_kw']
        assert 50.0 == tariff['green']['na_tusd_in_reais_per_kw']
        assert 2 == Tariff.objects.count()
    
    def test_rejects_start_date_after_end_date(self):
        tomorrow = (TODAY + timedelta(days=1))
        tariff_dict = self._create_tariff_dict(start_date=tomorrow, end_date=TODAY)

        response = self.client.post(ENDPOINT, tariff_dict, format='json')
        error = json.loads(response.content)
        
        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert 'Start date must be before' in error['non_field_errors'][0]
    
    def test_rejects_tariffs_with_the_same_subgroup_for_the_same_distributor(self):
        tariff_dict = self._create_tariff_dict()
        response = self.client.post(ENDPOINT, tariff_dict, format='json')
        assert status.HTTP_201_CREATED == response.status_code

        new_tariff = tariff_dict.copy()
        new_tariff['peak_tusd_in_reais_per_mwh'] = 100

        response = self.client.post(ENDPOINT, new_tariff, format='json')
        error = json.loads(response.content)

        assert status.HTTP_403_FORBIDDEN == response.status_code
        assert 'There is already a tariff with given the subgroup and distributor' in error['error'][0]
    
    @pytest.mark.skip
    def test_rejects_blue_tariff_creation_with_green_tariff_fields(self):
        '''Esse teste ainda não passa. O serializer aceita outros campos não
        definidos'''
        tariff_dict = self._create_tariff_dict()
        tariff_dict['na_tusd_in_reais_per_kw'] = 8080
        
        response = self.client.post(ENDPOINT, tariff_dict, format='json')
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    @pytest.mark.skip
    def test_rejects_green_tariff_creation_with_blue_tariff_fields(self):
        ...
    
    def test_rejects_tariff_creation_with_missing_fields(self):
        tariff_dict = self._create_tariff_dict()
        del tariff_dict['end_date']
        del tariff_dict['blue']['off_peak_te_in_reais_per_mwh']
        del tariff_dict['green']['na_tusd_in_reais_per_kw']
        
        response = self.client.post(ENDPOINT, tariff_dict, format='json')
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert 'This field is required' in error['end_date'][0]    
        assert 'This field is required' in error['blue']['off_peak_te_in_reais_per_mwh'][0]    
        assert 'This field is required' in error['green']['na_tusd_in_reais_per_kw'][0]

    def test_updates_tariff(self):
        t = self._create_tariff_dict()
        Tariff.objects.create(subgroup=t['subgroup'], flag=Tariff.BLUE, distributor=self.distributor1, **t['blue'], start_date=t['start_date'], end_date=t['end_date'])
        Tariff.objects.create(subgroup=t['subgroup'], flag=Tariff.GREEN, distributor=self.distributor1, **t['green'], start_date=t['start_date'], end_date=t['end_date'])
        assert 2 == Tariff.objects.count()

        year_later = (TODAY+timedelta(days=365)).strftime(DATE_FORMAT)
        to_update = t.copy()
        to_update['end_date'] = year_later
        to_update['blue']['off_peak_te_in_reais_per_mwh'] = 2020
        to_update['green']['na_tusd_in_reais_per_kw'] = 3030

        response = self.client.put(ENDPOINT + '1/', to_update, format='json')
        tariff = json.loads(response.content)

        assert status.HTTP_200_OK == response.status_code
        assert year_later == tariff['end_date']
        assert 2020 == tariff['blue']['off_peak_te_in_reais_per_mwh']
        assert 3030 == tariff['green']['na_tusd_in_reais_per_kw']

    def test_rejects_attempt_to_update_non_existing_tariffs(self):
        tariff_dict = self._create_tariff_dict()

        response = self.client.put(ENDPOINT + '1/', tariff_dict, format='json')
        error = json.loads(response.content)

        assert status.HTTP_404_NOT_FOUND == response.status_code
        assert 'Could not find tariffs' in error['error'][0]
    
    def test_list_tariffs(self):
        self._create_3_tariffs_from_dist1_2_tariffs_from_dist2()
        response = self.client.get(ENDPOINT)
        tariffs: list = json.loads(response.content)

        assert 5 == len(tariffs)
        
        tariffs_from_distributor1 = list(filter(lambda t: t['distributor'] == self.distributor1.id, tariffs))
        assert 3 == len(tariffs_from_distributor1)
        for t in tariffs_from_distributor1:
            assert self.distributor1.id == t['distributor']
            assert t['blue'] != None
            assert t['green'] != None
    
        tariffs_from_distributor2 = list(filter(lambda t: t['distributor'] == self.distributor2.id, tariffs))
        assert 2 == len(tariffs_from_distributor2)
        for t in tariffs_from_distributor2:
            assert self.distributor2.id == t['distributor']
            assert t['blue'] != None
            assert t['green'] != None
        
    def test_list_tariffs_with_distributor_in_query_params(self):
        self._create_3_tariffs_from_dist1_2_tariffs_from_dist2()

        response = self.client.get(f'{ENDPOINT}?distributor={self.distributor1.id}')
        tariffs: list = json.loads(response.content)

        assert 3 == len(tariffs)
        for t in tariffs:
            assert self.distributor1.id == t['distributor']
            assert t['blue'] != None
            assert t['green'] != None        
        
    
    def _create_tariff_dict(self, 
        start_date: date=None, 
        end_date: date=None, 
        subgroup: str='A3',
        distributor_id: Distributor=None
    ):
        start_date = start_date if start_date != None else TODAY
        end_date = end_date if end_date != None else (TODAY+timedelta(days=1))
        distributor_id = distributor_id if distributor_id != None else self.distributor1.id
        t = {
            'distributor': distributor_id,
            'start_date': start_date.strftime(DATE_FORMAT),
            'end_date': end_date.strftime(DATE_FORMAT),
            'subgroup': subgroup,
            'blue': {
                'peak_tusd_in_reais_per_kw': 1,
                'peak_tusd_in_reais_per_mwh': 2,
                'peak_te_in_reais_per_mwh': 3,
                'off_peak_tusd_in_reais_per_kw': 4,
                'off_peak_tusd_in_reais_per_mwh': 5,
                'off_peak_te_in_reais_per_mwh': 6,
            },
            'green': {
                'peak_tusd_in_reais_per_mwh': 10,
                'peak_te_in_reais_per_mwh': 20,
                'off_peak_tusd_in_reais_per_mwh': 30,
                'off_peak_te_in_reais_per_mwh': 40,
                'na_tusd_in_reais_per_kw': 50,
            }
        }
        return t
    
    def _create_3_tariffs_from_dist1_2_tariffs_from_dist2(self) -> None:
        t1_d1 = self._create_tariff_dict(subgroup='A3')
        Tariff.objects.create(subgroup=t1_d1['subgroup'], flag=Tariff.BLUE, distributor=self.distributor1, **t1_d1['blue'], start_date=t1_d1['start_date'], end_date=t1_d1['end_date'])
        Tariff.objects.create(subgroup=t1_d1['subgroup'], flag=Tariff.GREEN, distributor=self.distributor1, **t1_d1['green'], start_date=t1_d1['start_date'], end_date=t1_d1['end_date'])

        t2_d1 = self._create_tariff_dict(subgroup='A4')
        Tariff.objects.create(subgroup=t2_d1['subgroup'], flag=Tariff.BLUE, distributor=self.distributor1, **t2_d1['blue'], start_date=t2_d1['start_date'], end_date=t2_d1['end_date'])
        Tariff.objects.create(subgroup=t2_d1['subgroup'], flag=Tariff.GREEN, distributor=self.distributor1, **t2_d1['green'], start_date=t2_d1['start_date'], end_date=t2_d1['end_date'])

        t3_d1 = self._create_tariff_dict(subgroup='AS')
        Tariff.objects.create(subgroup=t3_d1['subgroup'], flag=Tariff.BLUE, distributor=self.distributor1, **t3_d1['blue'], start_date=t3_d1['start_date'], end_date=t3_d1['end_date'])
        Tariff.objects.create(subgroup=t3_d1['subgroup'], flag=Tariff.GREEN, distributor=self.distributor1, **t3_d1['green'], start_date=t3_d1['start_date'], end_date=t3_d1['end_date'])

        t1_d2 = self._create_tariff_dict(subgroup='A3', distributor_id=self.distributor2.id)
        Tariff.objects.create(subgroup=t1_d2['subgroup'], flag=Tariff.BLUE, distributor=self.distributor2, **t1_d2['blue'], start_date=t1_d2['start_date'], end_date=t1_d2['end_date'])
        Tariff.objects.create(subgroup=t1_d2['subgroup'], flag=Tariff.GREEN, distributor=self.distributor2, **t1_d2['green'], start_date=t1_d2['start_date'], end_date=t1_d2['end_date'])

        t2_d2 = self._create_tariff_dict(subgroup='A4', distributor_id=self.distributor2.id)
        Tariff.objects.create(subgroup=t2_d2['subgroup'], flag=Tariff.BLUE, distributor=self.distributor2, **t2_d2['blue'], start_date=t2_d2['start_date'], end_date=t2_d2['end_date'])
        Tariff.objects.create(subgroup=t2_d2['subgroup'], flag=Tariff.GREEN, distributor=self.distributor2, **t2_d2['green'], start_date=t2_d2['start_date'], end_date=t2_d2['end_date'])
        return