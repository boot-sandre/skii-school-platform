from django.db import models
from decimal import Decimal as Deci
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

from apps.skii_school_core.entities import (
    RessourceEntity,
    AgentEntity,
    UUIDEntity,
    DisplayEntity,
    DescriptionEntity,
    StateEntity,
    AgendaEntity,
)

from django.contrib.auth import get_user_model


User = get_user_model()


##################
# AGENT ENTITIES #
##################


class StudentAgent(AgentEntity):
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Student(s)")
        ordering = ["-last_modified", "-created"]


class TeacherAgent(AgentEntity):
    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teacher(s)")
        ordering = ["-last_modified", "-created"]


######################
# RESSOURCE ENTITIES #
######################


class MoneyRessource(RessourceEntity):
    class Meta:
        verbose_name = _("Money")
        verbose_name_plural = _("Money(s)")
        ordering = ["-last_modified", "-created", "amount"]

    amount = MoneyField(
        verbose_name=_("Money amount"),
        max_digits=18,
        decimal_places=6,
        default=Deci(0.0),
        default_currency="EUR",
    )


class TimeRessource(RessourceEntity):
    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Time(s)")
        ordering = ["-last_modified", "-created", "amount"]

    amount = models.DecimalField(
        verbose_name=_("Time recorded (seconds)"),
        default=Deci(0.0),
        max_digits=20,
        decimal_places=6,
    )


####################
# EVENT / LOCATION #
####################
class Event(StateEntity, AgendaEntity):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Event(s)")
        ordering = ["state", "-created", "-start", "-stop", "label"]

    editor = models.ForeignKey(User, on_delete=models.PROTECT)
    agent_invited = models.ManyToManyField(
        User, blank=True, related_name="events_linked"
    )

    def __str__(self):
        return f"[{self.state}]{str(self.label)}:  Date {self.start} / {self.stop} "


class Location(UUIDEntity, DisplayEntity):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Location(s)")
        ordering = ["-created", "-last_modified", "country", "city", "label"]

    address1 = models.CharField(verbose_name=_("Address line 1"), max_length=255)
    address2 = models.CharField(
        max_length=255, verbose_name=_("Address line 2"), blank=True, null=True
    )
    city = models.CharField(verbose_name=_("City"), max_length=255)
    country = CountryField(verbose_name=_("Country"), default="EN")

    def __str__(self):
        return f"{self.label}:ModelSchema {self.city} / {self.country.name}"
