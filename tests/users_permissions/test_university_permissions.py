import json
import pytest
from datetime import date
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser, UniversityUser
from universities.models import ConsumerUnit, University

from tests.test_utils.create_objects_util import CreateObjectsUtil

ENDPOINT = '/api/users/'
PASSWORD = CreateObjectsUtil.login_university_user['password']

TOKEN_ENDPOINT = '/api/token/'
ENDPOINT_UNIVERSITY = '/api/universities/'

@pytest.mark.django_db
class TestUniversityPermissions:
    def setup_method(self):
        self.client = APIClient()
        self.university = University(name='UnB', cnpj='00038174000143')
        self.university.save()

        self.email_super_user = 'super_user@email.com'
        self.email_university_admin_user = 'university_admin@email.com'
        self.email_university_user = 'university_user@email.com'

        self.super_user = CustomUser.objects.create_superuser(email=self.email_super_user, password=PASSWORD)

        self.university_admin_user = UniversityUser.objects.create(
            email=self.email_university_admin_user, password=PASSWORD, type=CustomUser.university_admin_user_type, university=self.university)

        self.university_user = UniversityUser.objects.create(
            email=self.email_university_user, password=PASSWORD, type=CustomUser.university_user_type, university=self.university)

    def test_super_user_already_created(self):
        assert type(self.super_user) == CustomUser
        assert self.super_user.email == self.email_super_user
        assert self.super_user.type == CustomUser.super_user_type

    def test_university_admin_user_already_created(self):
        assert type(self.university_admin_user) == UniversityUser
        assert self.university_admin_user.email == self.email_university_admin_user
        assert self.university_admin_user.university == self.university
        assert self.university_admin_user.type == CustomUser.university_admin_user_type

    def test_university_user_already_created(self):
        assert type(self.university_user) == UniversityUser
        assert self.university_user.email == self.email_university_user
        assert self.university_user.university == self.university
        assert self.university_user.type == CustomUser.university_user_type
