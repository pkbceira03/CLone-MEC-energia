import pytest
from rest_framework.test import APIClient

from contracts.models import Contract

from tests.test_utils.create_objects_util import CreateObjectsUtil
from tests.test_utils.contract_test_utils.create_contract_unit_test_util import CreateContractTestUtil

@pytest.mark.django_db
class TestContractSubGroup:
    def setup_method(self):
        self.university, self.user = CreateObjectsUtil.create_university_and_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_university_user['email'], 
            password = CreateObjectsUtil.login_university_user['password'])

        self.university_to_be_created = {
            'name': 'Universidade de Brasília',
            'cnpj': '00038174000143'
        }

        (self.consumer_unit_test_dict,
        self.consumer_unit_test) = CreateObjectsUtil.create_consumer_unit_object(
                                        consumer_unit_dict_index = 0,
                                        university = self.university)

        _, self.distributor = CreateObjectsUtil.create_distributor_object(self.university, 0)

        self.contract_test_1 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 0, distributor = self.distributor,
                                consumer_unit = self.consumer_unit_test)

        self.contract_test_2 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 1, distributor = self.distributor,
                                consumer_unit = self.consumer_unit_test)

        self.contract_test_3 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 2, distributor = self.distributor,
                                consumer_unit = self.consumer_unit_test)


    def test_read_contract_subgroup_A3(self):
        assert self.contract_test_3.supply_voltage == 69
        assert self.contract_test_3.subgroup == 'A3'
    
    def test_read_contract_subgroup_A2(self):
        assert self.contract_test_1.supply_voltage == 100.00
        assert self.contract_test_1.subgroup == 'A2'

    def test_read_contract_subgroup_A1(self):
        assert self.contract_test_2.supply_voltage == 250.00
        assert self.contract_test_2.subgroup == 'A1'

    def test_throws_exception_when_suply_voltage_does_not_match_ranges_in_create_contract(self):
        with pytest.raises(Exception) as e:
            CreateObjectsUtil.create_contract_object(
                contract_dict_index = 2, distributor = self.distributor,
                consumer_unit = self.consumer_unit_test)

        assert 'Already have the contract in this date' in str(e.value)

    def test_throws_exception_when_suply_voltage_does_not_match_subgroup_ranges(self):
        with pytest.raises(Exception) as e:
            CreateContractTestUtil.create_contract_with_wrong_suply_voltage(distributor=self.distributor, consumer_unit=self.consumer_unit_test)

        assert 'Subgroup not found' in str(e.value)
        assert 3 == Contract.objects.all().count()