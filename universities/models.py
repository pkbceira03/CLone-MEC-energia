from django.db import models
from django.utils.translation import gettext_lazy as _


class University(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Nome'),
        help_text=_('Nome da universidade por extenso')
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
        help_text=_('Cheque a conta de luz para obter o código da Unidade Consumidora. Insira apenas números')
    )

    is_active = models.BooleanField(default=True)

    university = models.ForeignKey(
        University,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name='Universidade',
        related_name='consumer_units',
        help_text=_('Uma Unidade Consumidora deve estar ligada a uma Universidade')
    )

    created_on = models.DateField(auto_now_add=True)

    def __repr__(self) -> str:
        return f'UC {self.name}'
