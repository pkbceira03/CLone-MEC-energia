import pytest
from rest_framework.test import APIClient

from contracts.models import Contract

from utils.date_util import DateUtils

from tests.test_utils.create_objects_util import CreateObjectsUtil

@pytest.mark.django_db
class TestContractEndpoint:
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
                                contract_dict_index = 0, distributor=self.distributor,
                                consumer_unit = self.consumer_unit_test)

        self.contract_test_2 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 1, distributor=self.distributor,
                                consumer_unit = self.consumer_unit_test)

        self.contract_test_3 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 2, distributor=self.distributor,
                                consumer_unit = self.consumer_unit_test)

        self.contract_test_4 = CreateObjectsUtil.create_contract_object(
                                contract_dict_index = 3, distributor=self.distributor,
                                consumer_unit = self.consumer_unit_test)


    def test_create_contract_and_set_last_contract_end_date_1(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_2.start_date)

        contract_test_1 = Contract.objects.get(id = self.contract_test_1.id)

        assert contract_test_1.end_date == end_date

    def test_create_contract_and_set_last_contract_end_date_2(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_3.start_date)

        contract_test_2 = Contract.objects.get(id = self.contract_test_2.id)

        assert contract_test_2.end_date == end_date

    def test_create_contract_and_set_last_contract_end_date_3(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_4.start_date)

        contract_test_3 = Contract.objects.get(id = self.contract_test_3.id)

        assert contract_test_3.end_date == end_date

    def test_throws_exception_create_contract_with_start_date_not_valid(self):
        with pytest.raises(Exception) as e:
            CreateObjectsUtil.create_contract_object(
                contract_dict_index = 5, distributor=self.distributor,
                consumer_unit = self.consumer_unit_test)

        assert 'Already have the contract in this date' in str(e.value)