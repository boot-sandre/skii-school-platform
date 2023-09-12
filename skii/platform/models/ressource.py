######################
# RESSOURCE ENTITIES #
######################
from decimal import Decimal as Deci

from django.db import models
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField

from skii.platform.entities import RessourceEntity


class MoneyRessource(RessourceEntity):
    class Meta:
        verbose_name = _("Money")
        verbose_name_plural = _("Money(s)")
        ordering = ["-last_modified", "-created", "amount"]

    amount = MoneyField(
        verbose_name=_("Money amount"),
        max_digits=18,
        decimal_places=2,
        default=Deci(0.0),
        default_currency="EUR",
    )


class TimeRessource(RessourceEntity):
    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Time(s)")
        ordering = ["-last_modified", "-created", "amount"]

    amount = models.DecimalField(
        verbose_name=_("Time delta in seconds"),
        default=Deci(0.0),
        max_digits=20,
        decimal_places=6,
    )
