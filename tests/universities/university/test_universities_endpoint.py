import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

ENDPOINT = '/api/universities/'

from tests.test_utils.university_test_utils.create_university_test_util import CreateUniversityTestUtil
from tests.test_utils.create_objects_util import CreateObjectsUtil

@pytest.mark.django_db
class TestUniversitiesEndpoint:
    def setup_method(self):
        self.university = CreateObjectsUtil.create_university_object() 
        self.user = CreateObjectsUtil.create_super_user()
        
        self.client = APIClient()
        self.client.login(
            email = CreateObjectsUtil.login_super_user['email'], 
            password = CreateObjectsUtil.login_super_user['password'])

        self.university_to_be_created = {
            'name': 'Universidade de Brasília',
            'cnpj': '00038174000143'
        }

    def test_create_university(self):
        response = self.client.post(ENDPOINT, self.university_to_be_created)

        created_university = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert created_university['cnpj'] == self.university_to_be_created['cnpj']

    def test_reject_university_with_invalid_cnpj(self):
        self.university_to_be_created['cnpj'] = 'F0038174000143'

        response = self.client.post(ENDPOINT, self.university_to_be_created)

        error_json = json.loads(response.content)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'must contain exactly 14 numerical digits' in error_json['cnpj'][0]

    def test_reject_attempt_to_delete_university(self):
        response = self.client.delete(ENDPOINT, CreateUniversityTestUtil.university_dict)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_reject_attempt_to_delete_university_by_id(self):
        delete_endpoint = f'{ENDPOINT}{self.university.id}/'
        response = self.client.delete(delete_endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
