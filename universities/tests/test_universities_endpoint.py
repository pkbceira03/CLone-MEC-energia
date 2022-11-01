import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import UniversityUser
from universities.models import University

ENDPOINT = '/api/universities/'
EMAIL = 'admin@admin.com'
PASSWORD = 'password'


@pytest.mark.django_db
class TestUniversitiesEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.existing_university_dict = {
            'name': 'Universidade de São Paulo',
            'cnpj': '63025530000104'
        }
        self.existing_university = University(**self.existing_university_dict)
        self.existing_university.save()

        self.user = UniversityUser.objects.create_user(
            email=EMAIL, password=PASSWORD, university=self.existing_university)
        self.client.login(email=EMAIL, password=PASSWORD)
        self.university_to_be_created = {
            'name': 'Universidade de Brasília',
            'cnpj': '00038174000143'
        }

    def test_creates_university(self):
        response = self.client.post(ENDPOINT, self.university_to_be_created)

        created_university = json.loads(response.content)
        assert created_university['cnpj'] == self.university_to_be_created['cnpj']
        assert response.status_code == status.HTTP_201_CREATED

    def test_rejects_university_with_invalid_cnpj(self):
        self.university_to_be_created['cnpj'] = 'F0038174000143'

        response = self.client.post(ENDPOINT, self.university_to_be_created)

        error_json = json.loads(response.content)
        assert 'must contain exactly 14 numerical digits' in error_json['cnpj'][0]
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_attempt_to_delete_university(self):
        response = self.client.delete(ENDPOINT, self.existing_university_dict)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_rejects_attempt_to_delete_university_by_id(self):
        delete_endpoint = f'{ENDPOINT}{self.existing_university.id}/'
        response = self.client.delete(delete_endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
