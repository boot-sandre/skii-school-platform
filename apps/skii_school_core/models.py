from django.db import models
from decimal import Decimal as Deci
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _

from apps.skii_school_core.entities import (
    RessourceEntity,
    AgentEntity,
    UUIDEntity,
    StateEntity,
    AgendaEntity,
    CMSDisplayEntity,
    NomenclatureEntity,
    ContentEntity,
    VisualEntity,
    UUIDLabelEntity,
    CMSUUIDEntity,
    GeoCoordinateEntity
)

from django.contrib.auth import get_user_model


User = get_user_model()


##################
# AGENT ENTITIES #
##################

class VisualAlbum(CMSUUIDEntity):
    class Meta:
        verbose_name = _("Visual Album")
        verbose_name_plural = _("Visual Album(s)")
        ordering = ["-last_modified", "-created", "title"]


def get_default_album():
    return VisualAlbum.objects.first().uuid


class VisualElement(VisualEntity):
    class Meta:
        verbose_name = _("Visual Album Picture")
        verbose_name_plural = _("Visual Album Picture(s)")
        ordering = ["-last_modified", "-created", "title"]

    album = models.ForeignKey(
        VisualAlbum, on_delete=models.CASCADE, related_name="items",
        verbose_name=_("Album"), default=get_default_album)

    def __str__(self):
        return f"[{self.uuid}] {self.title[:30]} from album {self.album.title[:30]}"


class VisualPicture(VisualEntity):

    @property
    def picture_url(self):
        return self.picture.url

    class Meta:
        verbose_name = _("Visual Picture")
        verbose_name_plural = _("Visual Picture(s)")
        ordering = ["-last_modified", "-created", "title"]


class GeoCoordinate(GeoCoordinateEntity):
    class Meta:
        verbose_name = _("Geographic coordinate")
        verbose_name_plural = _("Geographic coordinate(s)")
        ordering = ["latitude", "longitude"]

    def __str__(self):
        return f"{self.latitude} / {self.longitude} "


class StudentAgent(AgentEntity):
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Student(s)")
        ordering = ["-last_modified", "-created", "user__username"]


class TeacherAgent(AgentEntity):
    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teacher(s)")
        ordering = ["-last_modified", "-created", "user__username"]


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
        ordering = ["state", "-created", "-start", "-stop", "title"]

    teacher = models.ForeignKey(TeacherAgent, on_delete=models.PROTECT)
    students = models.ManyToManyField(
        StudentAgent, blank=True, related_name="events_linked"
    )

    def __str__(self) -> str:
        start_datetime = self.start.strftime(format="%Y-%m-%d %H:%M:%S")
        stop_datetime = self.stop.strftime(format="%Y-%m-%d %H:%M:%S")
        return f"{self.pk} [{self.state}] {str(self.title)}: {start_datetime} / {stop_datetime} "


class Location(UUIDLabelEntity, ContentEntity):
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Location(s)")
        ordering = ["-last_modified", "-created", "country", "city", "label"]

    address1 = models.CharField(verbose_name=_("Address line 1"), max_length=255)
    address2 = models.CharField(
        max_length=255, verbose_name=_("Address line 2"), blank=True, null=True
    )
    city = models.CharField(verbose_name=_("City"), max_length=255)
    country = CountryField(verbose_name=_("Country"), default="RO")
    cover = models.ForeignKey(VisualPicture, on_delete=models.SET_NULL,
                              blank=True, null=True)
    illustration = models.ForeignKey(VisualAlbum, on_delete=models.SET_NULL,
                                     blank=True, null=True)
    coordinate = models.ForeignKey(GeoCoordinate, on_delete=models.PROTECT,
                                   blank=True, null=True)

    def __str__(self):
        return f"{self.label} {self.city} / {self.country.name}"


