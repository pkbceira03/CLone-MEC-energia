import pytest

from contracts.models import Contract

from tests.test_utils.create_objects_util import CreateObjectsUtil

@pytest.mark.django_db
class TestContractCreation:
    def setup_method(self):
        self.university = CreateObjectsUtil.create_university_object()
        _, self.distributor = CreateObjectsUtil.create_distributor_object(self.university, 0)
        (self.consumer_unit_dict,
        self.consumer_unit) = CreateObjectsUtil.create_consumer_unit_object(
                                university = self.university)