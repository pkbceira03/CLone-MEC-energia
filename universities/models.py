from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

from contracts.models import Contract, EnergyBill
from .recommendation import Recommendation
from utils.energy_bill_util import EnergyBillUtils

class University(models.Model):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('Nome'),
        help_text=_('Nome da universidade por extenso')
    )

    acronym = models.CharField(
        null=True,
        max_length=50,
        unique=True,
        verbose_name=_('Sigla'),
        help_text=_('Exemplo: UnB, UFSC, UFB')
    )

    cnpj = models.CharField(
        max_length=14,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('CNPJ'),
        help_text=_('14 números sem caracteres especiais')
    )

    created_on = models.DateField(auto_now_add=True)

class ConsumerUnit(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Nome'),
        help_text=_('Nome da Unidade Consumidora. Ex: Darcy Ribeiro')
    )

    code = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_('Código da Unidade Consumidora'),
        help_text=_(
            'Cheque a conta de luz para obter o código da Unidade Consumidora. Insira apenas números')
    )

    is_active = models.BooleanField(default=True)

    university = models.ForeignKey(
        University,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Universidade',
        related_name='consumer_units',
        help_text=_(
            'Uma Unidade Consumidora deve estar ligada a uma Universidade')
    )

    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def current_contract(self) -> Contract:
        return self.contract_set.all().order_by('start_date').last()

    @property
    def oldest_contract(self):
        return self.contract_set.all().order_by('start_date').first()

    @property
    def date(self):
        if not self.current_contract:
            return 'Unidade Consumidora sem Contrato'
        
        return self.oldest_contract.start_date

    @property
    def is_current_energy_bill_filled(self):
        if EnergyBill.get_energy_bill(
            self.id,
            date.today().month,
            date.today().year):
            
            return True
        return False

    @property
    def pending_energy_bills_number(self):
        if not self.current_contract:
            return 'Unidade Consumidora sem Contrato'

        pending_bills_number = 0
        energy_bills = Recommendation.get_energy_bills_for_recommendation(self.id)
        
        for energy_bill in energy_bills:
            if energy_bill['energy_bill'] == None:
                pending_bills_number += 1

        return pending_bills_number

    @classmethod
    def create_consumer_unit_and_contract(cls, data_consumer_unit, data_contract):
        created_consumer_unit = None

        try:
            created_consumer_unit = ConsumerUnit(
                university_id = data_consumer_unit['university'],
                name = data_consumer_unit['name'],
                code = data_consumer_unit['code'],
                is_active = data_consumer_unit['is_active'],
            )

            created_contract = Contract(
                consumer_unit = created_consumer_unit,
                distributor_id = data_contract['distributor'],
                start_date = data_contract['start_date'],
                tariff_flag = data_contract['tariff_flag'],
                supply_voltage = data_contract['supply_voltage'],
                peak_contracted_demand_in_kw = data_contract['peak_contracted_demand_in_kw'],
                off_peak_contracted_demand_in_kw = data_contract['off_peak_contracted_demand_in_kw'],
            )
        except Exception as error:
            raise Exception('error create consumer unit and contract: ' + str(error))

        created_consumer_unit.save()
        created_contract.save()

        return created_consumer_unit, created_contract

    @classmethod
    def edit_consumer_unit_and_contract(cls, data_consumer_unit, data_contract):

        try:
            consumer_unit = ConsumerUnit.objects.get(id = data_consumer_unit['consumer_unit_id'])
            contract = Contract.objects.get(id = data_contract['contract_id'], consumer_unit = consumer_unit)
            
            consumer_unit.name = data_consumer_unit['name']
            consumer_unit.code = data_consumer_unit['code']
            consumer_unit.is_active = data_consumer_unit['is_active']

            contract.start_date = data_contract['start_date']
            contract.tariff_flag = data_contract['tariff_flag']
            contract.supply_voltage = data_contract['supply_voltage']
            contract.peak_contracted_demand_in_kw = data_contract['peak_contracted_demand_in_kw']
            contract.off_peak_contracted_demand_in_kw = data_contract['off_peak_contracted_demand_in_kw']

            consumer_unit.save()
            contract.save()
        except Exception as error:
            raise Exception('error edit consumer unit and contract: ' + str(error))

        return consumer_unit, contract

    def get_energy_bills_by_year(self, year):
        if year < self.date.year or year > date.today().year:
            raise Exception('Consumer User do not have Energy Bills this year')

        energy_bills_dates = EnergyBillUtils.generate_dates_by_year(year)
        
        for object in energy_bills_dates:
            object['energy_bill'] = None

            energy_bill = EnergyBill.get_energy_bill(
                self.id,
                object['month'], 
                object['year'])
            
            if energy_bill:
                object['energy_bill'] = EnergyBillUtils.energy_bill_dictionary(energy_bill)

        return list(energy_bills_dates)
    
    def get_energy_bills_pending(self):
        if not self.current_contract:
            return 'Unidade Consumidora sem Contrato'

        energy_bills_pending = []
            
        energy_bills = self.get_energy_bills_for_recommendation()

        for energy_bill in energy_bills:
            if energy_bill['energy_bill'] == None:
                energy_bills_pending.append(energy_bill)

        return list(energy_bills_pending)
    
    def get_energy_bills_for_recommendation(self):
        if not self.current_contract:
            return 'Unidade Consumidora sem Contrato'

        energy_bills = Recommendation.get_energy_bills_for_recommendation(self.id)

        return energy_bills

    def get_all_energy_bills(self):
        if not self.current_contract:
            return 'Unidade Consumidora sem Contrato'

        energy_bills = Recommendation.get_all_energy_bills_by_consumer_unit(self.id, self.date)

        return energy_bills

    def __repr__(self) -> str:
        return f'UC {self.name}'
