import pytest
import json

from rest_framework import status
from rest_framework.test import APIClient

from users.models import UniversityUser
from universities.models import University
from tariffs.models import Distributor

from tariffs.tests.utils import create_blue_tariff


ENDPOINT = '/api/distributors/'
EMAIL = 'admin@admin.com'
PASSWORD = 'password'


@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.client = APIClient()
        self.university_dict = {
            'name': 'Universidade de São Paulo',
            'cnpj': '63025530000104'
        }

        self.university = University.objects.create(**self.university_dict)

        self.user = UniversityUser.objects.create_user(
            email=EMAIL, password=PASSWORD, university=self.university)
        assert self.client.login(email=EMAIL, password=PASSWORD)

    def test_creates_distributor(self):
        response = self.client.post(ENDPOINT,
            {'name': 'Distribuidora', 'cnpj': '00038174000143',
            'university': self.university.id})

        created_distributor = json.loads(response.content)

        assert status.HTTP_201_CREATED == response.status_code
        assert 'Distribuidora' == created_distributor['name']

    def test_cannot_create_distributors_with_same_cnpj(self):
        dis_1 = {'name': 'Dis 1', 'cnpj': '00038174000143', 'university': self.university}
        dis_2 = {'name': 'Dis 2', 'cnpj': '00038174000143', 'university': self.university.id}

        Distributor.objects.create(**dis_1)
        response = self.client.post(ENDPOINT, dis_2)

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_cannot_delete_distributor_with_dependent_tariff(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        create_blue_tariff(dis.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')
        assert status.HTTP_400_BAD_REQUEST == response.status_code
    
    def test_deletes_distributor_with_no_tariffs(self):
        dis = Distributor.objects.create(name='Dis', cnpj='00038174000143', university_id=self.university.id)

        response = self.client.delete(ENDPOINT + f'{dis.id}/')

        assert status.HTTP_204_NO_CONTENT == response.status_code