from decimal import Decimal
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _

from skii.platform.entities import (
    VisualEntity,
    CMSUUIDEntity,
    GeoCoordinateEntity,
)


class VisualAlbum(CMSUUIDEntity):
    class Meta:
        verbose_name = _("Visual Album")
        verbose_name_plural = _("Visual Album(s)")
        ordering = ["-last_modified", "-created", "title"]


def get_default_album():
    """Provide the first Album to link VisualElement."""
    return VisualAlbum.objects.first().guid


class VisualElement(VisualEntity):
    @property
    def picture_url(self):
        return self.picture.url

    class Meta:
        verbose_name = _("Visual Album Picture")
        verbose_name_plural = _("Visual Album Picture(s)")
        ordering = ["-last_modified", "-created", "title"]

    album = models.ForeignKey(
        VisualAlbum,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Album"),
        default=get_default_album,
    )

    def __str__(self):
        return f"[{self.guid}] {self.title[:30]} from album {self.album.title[:30]}"


class VisualPicture(VisualEntity):
    @property
    def picture_url(self):
        return self.picture.url

    class Meta:
        verbose_name = _("Visual Picture")
        verbose_name_plural = _("Visual Picture(s)")
        ordering = ["-last_modified", "-created", "title"]


class GeoCoordinateManager(Manager):
    def get_by_natural_key(self, latitude: Decimal, longitude: Decimal):
        return self.get(latitude=latitude, longitude=longitude)


class GeoCoordinate(GeoCoordinateEntity):
    class Meta:
        verbose_name = _("Geographic coordinate")
        verbose_name_plural = _("Geographic coordinate(s)")
        ordering = ["latitude", "longitude"]

    objects = GeoCoordinateManager()

    def __str__(self):
        return f"{self.latitude} / {self.longitude} "

    def natural_key(self) -> tuple[Decimal, Decimal]:
        """Define a natural primary key.

        Limit id/guid exchange between front/back.
        """
        return self.latitude, self.longitude
