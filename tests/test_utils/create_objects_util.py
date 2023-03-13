from tests.test_utils.university_test_utils.create_university_test_util import CreateUniversityTestUtil
from tests.test_utils.users_test_utils.create_university_user_test_util import CreateUniversityUserTestUtil
from tests.test_utils.consumer_unit_test_utils.create_consumer_unit_test_util import CreateConsumerUnitTestUtil
from tests.test_utils.contract_test_utils.create_contract_unit_test_util import CreateContractTestUtil
from tests.test_utils.energy_bill_test_utils.create_energy_bill_unit_test_util import CreateEnergyBillTestUtil
from tests.test_utils.distributors_test_utils.create_distributors_test_util import CreateDistributorTestUtil
from tests.test_utils.users_test_utils.create_super_user_test_util import CreateSuperUserTestUtil

class CreateObjectsUtil:
    login_university_user = CreateUniversityUserTestUtil.university_user_dicts[0]
    login_super_user = CreateSuperUserTestUtil.super_user_dicts[0]

    def create_university_object():
        return CreateUniversityTestUtil.create_university()

    def create_university_user_object(university, index = None):
        if not index:
            index = 0
            
        return CreateUniversityUserTestUtil.create_university_user(index, university)

    def get_university_user_dict(index = None):
        if not index:
            index = 0

        return CreateUniversityUserTestUtil.get_university_user_dict(index)
    
    def create_super_user(index = None):
        return CreateSuperUserTestUtil.create_super_user(index)

    def create_university_and_user():
        university = CreateObjectsUtil.create_university_object()
        user = CreateObjectsUtil.create_university_user_object(university)

        return (university, user)

    def create_consumer_unit_object(university, consumer_unit_dict_index = None):
        if not consumer_unit_dict_index:
            consumer_unit_dict_index = 0

        consumer_unit_dict = CreateConsumerUnitTestUtil.get_consumer_unit_dict(consumer_unit_dict_index)
        consumer_unit = CreateConsumerUnitTestUtil.create_consumer_unit(consumer_unit_dict_index, university)
        
        return (consumer_unit_dict, consumer_unit)
    
    def create_distributor_object(university, distributor_dict_index=None):
        if not distributor_dict_index:
            distributor_dict_index = 0
        distributor_dict, distributor = CreateDistributorTestUtil.create_distributor(distributor_dict_index, university)
        return (distributor_dict, distributor)

    def create_contract_object(consumer_unit, distributor, contract_dict_index = None):
        if not contract_dict_index:
            contract_dict_index = 0

        contract = CreateContractTestUtil.create_contract(contract_dict_index, consumer_unit, distributor)

        return contract

    def create_contract_object_and_get_dict(consumer_unit, contract_dict_index = None):
        if not contract_dict_index:
            contract_dict_index = 0
        
        contract_dict = CreateContractTestUtil.get_contract_dict(contract_dict_index)
        contract = CreateContractTestUtil.create_contract(contract_dict_index, consumer_unit)

        return (contract_dict, contract)

    def create_energy_bill_by_index(energy_bill_dict_index, contract, consumer_unit):
        energy_bill = CreateEnergyBillTestUtil.create_energy_bill(energy_bill_dict_index, contract, consumer_unit)
        
        return energy_bill
