from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from universities.models import ConsumerUnit, University

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(_('Email is required'), unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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
    
