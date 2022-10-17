import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from universities.models import University, ConsumerUnit

TESTSERVER_ADDR = 'http://testserver/api/universities/'
ENDPOINT = '/api/consumer-units/'
USERNAME = 'admin'
EMAIL = 'admin@admin.com'
PASSWORD = 'admin@admin.com'


@pytest.mark.django_db
class TestConsumerUnitsEndpoint:
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username=USERNAME, email=EMAIL, password=PASSWORD)
        self.client.login(username=USERNAME, password=PASSWORD)
        university_dict = {
            'name': 'Universidade de Brasília',
            'cnpj': '00038174000143'
        }
        self.university = University(**university_dict)
        self.university.save()
        self.existing_consumer_unit_dict = {
            'name': 'Darcy Ribeiro',
            'code': '000000000',
            'created_on': '2022-10-02',
            'is_active': True,
            'university': self.university
        }
        self.existing_consumer_unit = ConsumerUnit(**self.existing_consumer_unit_dict)
        self.existing_consumer_unit.save()
        self.existing_university_id_as_url = f'{TESTSERVER_ADDR}{self.university.id}/'
        self.consumer_unit_to_be_created = {
            'name': 'Faculdade do Gama',
            'code': '111111111',
            'created_on': '2022-10-02',
            'is_active': True,
            'university': self.existing_university_id_as_url
        }

    def test_creates_consumer_unit(self):
        response = self.client.post(ENDPOINT, self.consumer_unit_to_be_created)
        created_consumer_unit = json.loads(response.content)

        assert created_consumer_unit['name'] == self.consumer_unit_to_be_created['name']
        assert created_consumer_unit['university'] == self.consumer_unit_to_be_created['university']
        assert response.status_code == status.HTTP_201_CREATED

    def test_rejects_deleting_consumer_unit(self):
        response = self.client.delete(ENDPOINT, self.existing_consumer_unit_dict)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_updates_is_active_of_consumer_unit_to_false(self):
        self.existing_consumer_unit_dict['is_active'] = False
        self.existing_consumer_unit_dict['university'] = self.existing_university_id_as_url
        
        response = self.client.put(
            f'{ENDPOINT}{self.existing_consumer_unit.id}/', 
            self.existing_consumer_unit_dict)

        assert response.status_code == status.HTTP_200_OK


    