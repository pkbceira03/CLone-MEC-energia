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

