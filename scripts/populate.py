#!/usr/local/bin/python

from universities.models import University, ConsumerUnit
from tariffs.models import Distributor

university = University.objects.create(
    name='Universidade de Brasília',
    acronym='UnB',
    cnpj='63025530000104'
)

unit = ConsumerUnit.objects.create(
    name='Darcy Ribeiro',
    code='1111111',
    is_active=True,
    university=university,
)

distributor = Distributor.objects.create(
    name='Neoenergia',
    cnpj='00038174000143',
    university=university,
)