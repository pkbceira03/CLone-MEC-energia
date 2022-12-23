import pytest
import json
from django.db.utils import IntegrityError
from rest_framework.test import APIClient

from tariffs.models import Distributor
from universities.models import University

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

        self.distributor_for_create = {
            'name': 'Distribuidora',
            'cnpj': '00038174000143',
            'university': self.university.id
        }

    def test_creates_distributor(self):
        response = self.client.post(ENDPOINT, self.distributor_for_create)

        created_distributor = json.loads(response.content)

        assert 'Distribuidora' == created_distributor['name']
    
    def test_can_create_the_same_distributor_for_different_unitversities(self):
        dis_1 = {'name': 'Dis 1', 'cnpj': '00038174000143', 'university_id': self.university.id}
        dis_2 = {'name': 'Dis 2', 'cnpj': '00038174000143', 'university_id': self.university.id}
        univ_2 = {'name': 'Universidade de Brasília', 'cnpj': '00038174000143'}

        University.objects.create(**univ_2)

        Distributor.objects.create(**dis_1)
        with pytest.raises(IntegrityError):
            Distributor.objects.create(**dis_2)

    def test_can_create_distributors_for_different_universities(self):
        university_2 = University.objects.create(name='Universidade de Brasília', cnpj='00038174000143')
        
        dis_1 = {'name': 'Dis 1', 'cnpj': '01083200000118', 'university': self.university}
        dis_2 = {'name': 'Dis 2', 'cnpj': '01083200000118', 'university': university_2}

        Distributor.objects.create(**dis_1)
        Distributor.objects.create(**dis_2)