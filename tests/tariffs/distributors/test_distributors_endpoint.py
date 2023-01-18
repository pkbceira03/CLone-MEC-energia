import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

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


    def test_cannot_delete_distributor_when_its_linked_to_a_consumer_units_current_contract(self):
        _, unit1 = CreateObjectsUtil.create_consumer_unit_object(self.university, 0)
        _, unit2 = CreateObjectsUtil.create_consumer_unit_object(self.university, 1)
        _, unit3 = CreateObjectsUtil.create_consumer_unit_object(self.university, 2)
        _, neoenergia = CreateObjectsUtil.create_distributor_object(self.university, 0)
        CreateObjectsUtil.create_contract_object(unit1, neoenergia, 0)
        CreateObjectsUtil.create_contract_object(unit2, neoenergia, 1)

        response = self.client.delete(ENDPOINT + f'{neoenergia.id}/')
        assert status.HTTP_400_BAD_REQUEST == response.status_code
        error = json.loads(response.content)
        
        assert 'There are active contracts associated to this distributor' in error['errors']
        assert unit1.id in error['consumer_units_ids']
        assert unit2.id in error['consumer_units_ids']
        assert unit3.id not in error['consumer_units_ids']
    
    def test_deletes_distributor_when_its_not_linked_to_any_contract(self):
        _, neoenergia = CreateObjectsUtil.create_distributor_object(self.university, 0)

        response = self.client.delete(ENDPOINT + f'{neoenergia.id}/')

        assert status.HTTP_204_NO_CONTENT == response.status_code
    
    @pytest.mark.skip
    def test_consumer_units_count_by_distributor(self):
        _, unit1 = CreateObjectsUtil.create_consumer_unit_object(self.university, 0)
        _, unit2 = CreateObjectsUtil.create_consumer_unit_object(self.university, 1)
        _, unit3 = CreateObjectsUtil.create_consumer_unit_object(self.university, 2)
        _, neoenergia = CreateObjectsUtil.create_distributor_object(self.university, 0)
        _, ceb = CreateObjectsUtil.create_distributor_object(self.university, 1)
        CreateObjectsUtil.create_contract_object(unit1, neoenergia, 0)
        CreateObjectsUtil.create_contract_object(unit2, ceb, 1)
        CreateObjectsUtil.create_contract_object(unit3, ceb, 2)

        response = self.client.get(ENDPOINT + f"?university_id={neoenergia.id}")
        assert status.HTTP_200_OK == response.status_code
        distributors = json.loads(response.content)

        neoenergia = list(filter(lambda dist: dist['id'] == neoenergia.id, distributors))[0]
        ceb = list(filter(lambda dist: dist['id'] == ceb.id, distributors))[0]

        # TODO Reavaliar condição de teste
        # assert 1 == neoenergia['consumer_units']
        # assert 2 == ceb['consumer_units']
    
    @pytest.mark.skip
    def test_zero_consumer_units_count_by_distributor(self):
        ...