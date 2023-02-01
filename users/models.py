from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from universities.models import ConsumerUnit, University

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
    ### User types
    super_user_type = 'super_user'
    university_admin_user_type = 'university_admin'
    university_user_type = 'university_user'

    all_user_types = [
        super_user_type,
        university_admin_user_type,
        university_user_type
    ]

    university_user_types = [
        university_admin_user_type,
        university_user_type
    ]

    username = None
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(_('Email is required'), unique=True, null=False)
    type = models.CharField(max_length=25, null=False, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    @classmethod
    def search_user_by_email(cls, email):
        return cls.objects.get(email = email)

    def change_user_last_login_time(self):
        self.last_login = timezone.now()
        self.save()

        return self

    def change_user_password_by_reset_password_token(self, new_password, reset_password_token):
        from .authentications import Password

        try:
            if Password.check_password_token_is_valid(self, reset_password_token):
                self.set_password(new_password)
                self.save()
            else:
                raise Exception('Reset password token is not valid')

            return self
        except Exception as error:
            raise Exception('Change User Password: ' + str(error))

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} [{self.email}]'


class UniversityUser(CustomUser):
    favorite_consumer_units = models.ManyToManyField(ConsumerUnit, blank=True)
    
    university = models.ForeignKey(
        University,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Universidade',
        help_text=_(
            'Um Usuário de Universidade deve estar ligado a uma Universidade')
    )

    def add_or_remove_favorite_consumer_unit(self, consumer_unit_id: int | str, action: str):
        unit = ConsumerUnit.objects.get(pk=consumer_unit_id)

        if unit.university.id != self.university.id:
            raise Exception('Cannot add/remove consumer unit from another university')

        if action == 'add':
            self.favorite_consumer_units.add(unit)
        elif action == 'remove':
            self.favorite_consumer_units.remove(unit)
        else:
            raise Exception('"action" field must be "add" or "remove"')
    
