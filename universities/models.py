from django.db import models
from mec_energia import settings
from django.utils.translation import gettext_lazy as _
from datetime import date

from .utils import EnergyBillsDates
from contracts.models import EnergyBill

class University(models.Model):
    name = models.CharField(
        max_length=50,
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
        unique=True,
        verbose_name=_('CNPJ'),
        help_text=_('14 números sem caracteres especiais')
    )


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

    created_on = models.DateField(auto_now_add=True)


    @property
    def oldest_contract(self):
        return self.contract_set.all().order_by('start_date').first()

    @property
    def date(self):
        if not self.oldest_contract:
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
        if not self.oldest_contract:
            return 'Unidade Consumidora sem Contrato'

        energy_bills = EnergyBillsDates.generate_dates_of_consumer_unit(self.date)

        pending_bills_number = 0
        for energy_bill in energy_bills:
            if not EnergyBill.get_energy_bill(
                self.id,
                energy_bill['month'], 
                energy_bill['year']):
                
                pending_bills_number += 1

        return pending_bills_number


    def __repr__(self) -> str:
        return f'UC {self.name}'
