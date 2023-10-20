# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
######################
# RESOURCES ENTITIES #
######################
from decimal import Decimal as Deci

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from djmoney.models.fields import MoneyField
from django.db.models import DecimalField, IntegerField

from skii.platform.entities import ResourceEntity
from skii.platform.models.common import VisualPicture, VisualAlbum, GeoCoordinate


class MoneyResource(ResourceEntity):
    class Meta:
        verbose_name = _("Money")
        verbose_name_plural = _("Money(s)")
        ordering = ["-last_modified", "-created", "value"]

    value = MoneyField(
        verbose_name=_("Money value"),
        max_digits=18,
        decimal_places=2,
        default=Deci(0.0),
        default_currency="EUR",
    )


class TimeResource(ResourceEntity):
    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Time(s)")
        ordering = ["-last_modified", "-created", "value"]

    value = DecimalField(
        verbose_name=_("Time delta in seconds"),
        default=Deci(0.0),
        max_digits=20,
        decimal_places=6,
    )


class LocationResource(ResourceEntity):
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
    cover = models.ForeignKey(
        VisualPicture, on_delete=models.SET_NULL, blank=True, null=True
    )
    illustration = models.ForeignKey(
        VisualAlbum, on_delete=models.SET_NULL, blank=True, null=True
    )
    coordinate = models.ForeignKey(
        GeoCoordinate, on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return f"{self.label} {self.city} / {self.country.name}"

    value = IntegerField(
        verbose_name=_("Time delta in seconds"),
        default=1,
        choices=[(0, "unused"), (1, "used")],
    )
