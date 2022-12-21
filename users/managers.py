from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from . import models
from utils.user_type_util import UserType

class CustomUserManager(BaseUserManager):
    def create(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        if not user.type:
            user.type = UserType.get_user_type_by_model(self.model)
        else:
            UserType.get_user_type(user.type)
        
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('type', models.CustomUser.super_user_type)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create(email, password, **extra_fields)
