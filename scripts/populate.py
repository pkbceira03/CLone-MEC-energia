#!/usr/local/bin/python
from datetime import date, timedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff

TODAY = date.today()
YEAR_LATER = TODAY + timedelta(days=365)

university = University.objects.create(
    name='Universidade de Brasília',
    acronym='UnB',
    cnpj='63025530000104'
)

university_user = UniversityUser.objects.create_user(
    university=university,
    password='user',
    email='user@user.com',
)

unit1 = ConsumerUnit.objects.create(
    name='Darcy Ribeiro',
    code='1111111',
    is_active=True,
    university=university,
)

unit2 = ConsumerUnit.objects.create(
    name='FGA',
    code='2222222',
    is_active=True,
    university=university,
)

unit3 = ConsumerUnit.objects.create(
    name='Campus Planaltina',
    code='3333333',
    is_active=True,
    university=university,
)

unit4 = ConsumerUnit.objects.create(
    name='Campus Ceilândia',
    code='4444444',
    is_active=True,
    university=university,
)

distributor1 = Distributor.objects.create(
    name='Neoenergia',
    cnpj='01083200000118',
    university=university,
)

distributor2 = Distributor.objects.create(
    name='CEB',
    cnpj='07522669000192',
    university=university,
)

contract1 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit1,
    distributor=distributor1,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=24,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

contract2 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit2,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=69,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

contract3 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit3,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=1.1,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

contract4 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit4,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=1.1,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

blue = {
    'peak_tusd_in_reais_per_kw':1,
    'peak_tusd_in_reais_per_mwh':2,
    'peak_te_in_reais_per_mwh':3,
    'off_peak_tusd_in_reais_per_kw':4,
    'off_peak_tusd_in_reais_per_mwh':5,
    'off_peak_te_in_reais_per_mwh':6,
}
green = {
    'peak_tusd_in_reais_per_mwh':10,
    'peak_te_in_reais_per_mwh':20,
    'off_peak_tusd_in_reais_per_mwh':30,
    'off_peak_te_in_reais_per_mwh':40,
    'na_tusd_in_reais_per_kw':50,
}

Tariff.objects.bulk_create([
    Tariff(subgroup='A4', distributor=distributor1, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A4', distributor=distributor1, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor1, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor1, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
])
