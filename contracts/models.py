from django.db import models
import datetime

from utils.subgroup_util import Subgroup

class Contract(models.Model):
    def save(self, *args, **kwargs):
        self.subgroup = Subgroup.get_subgroup(self.supply_voltage)

        super().save(*args, **kwargs)

    tariff_flag_choices = (
        ('G', 'Verde'),
        ('B', 'Azul'),
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    distributor = models.ForeignKey(
        'tariffs.Distributor',
        related_name='contracts',
        on_delete=models.PROTECT,
        null=True,
    )

    start_date = models.DateField(
        default=datetime.date.today,
        null=False,
        blank=False
    )
    
    end_date = models.DateField(
        null=True,
        blank=True
    )
    
    tariff_flag = models.CharField( 
        choices=tariff_flag_choices,
        max_length=1,
        null=True,
        blank=True
    )

    subgroup = models.CharField(
        max_length=3,
        null=True,
        blank=True
    )

    supply_voltage = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=False,
        blank=False
    )

    peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_contracted_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )


class EnergyBill(models.Model):

    contract = models.ForeignKey(
        'Contract',
        on_delete=models.PROTECT
    )

    consumer_unit = models.ForeignKey(
        'universities.ConsumerUnit',
        on_delete=models.PROTECT
    )

    date = models.DateField(
        null=True,
        blank=True
    )

    invoice_in_reais = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    is_atypical = models.BooleanField(
        default=False
    )

    peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_consumption_in_kwh = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    off_peak_measured_demand_in_kw = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    @classmethod
    def get_energy_bill(cls, consumer_unit_id, month, year):
        try:
            energy_bill = cls.objects.get(
                consumer_unit=consumer_unit_id,
                date__month=month,
                date__year=year)

            return energy_bill
        except:
            return None