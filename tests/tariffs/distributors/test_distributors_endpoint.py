import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tariffs.models import Distributor

from tests.test_utils.tariff_test_utils.create_tariff_test_util import CreateTariffTestUtil
from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/distributors/'

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])


    def test_cannot_delete_distributor_with_dependent_tariff(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        CreateTariffTestUtil.create_blue_tariff(dis.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')
        assert status.HTTP_400_BAD_REQUEST == response.status_code
    
    def test_deletes_distributor_with_no_tariffs(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')

        assert status.HTTP_204_NO_CONTENT == response.status_code
    
    def test_consumer_units_count_by_distributor(self):
        _, unit1 = CreateObjectsUtil.create_consumer_unit_object(self.university, 0)
        _, unit2 = CreateObjectsUtil.create_consumer_unit_object(self.university, 1)
        _, unit3 = CreateObjectsUtil.create_consumer_unit_object(self.university, 2)
        _, neoenergia = CreateObjectsUtil.create_distributor_object(self.university, 0)
        _, ceb = CreateObjectsUtil.create_distributor_object(self.university, 1)
        CreateObjectsUtil.create_contract_object(unit1, neoenergia, 0)
        CreateObjectsUtil.create_contract_object(unit2, ceb, 1)
        CreateObjectsUtil.create_contract_object(unit3, ceb, 2)

        response = self.client.get(ENDPOINT)

        assert status.HTTP_200_OK == response.status_code
        distributors = json.loads(response.content)

        neoenergia = list(filter(lambda dist: dist['id'] == neoenergia.id, distributors))[0]
        ceb = list(filter(lambda dist: dist['id'] == ceb.id, distributors))[0]

        assert 1 == neoenergia['consumer_units']
        assert 2 == ceb['consumer_units']
    
    @pytest.mark.skip
    def test_zero_consumer_units_count_by_distributor(self):
        ...