from django.db import models
from django.db.models import F, Q, CheckConstraint

from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


from skii.platform.entities import (
    StateEntity,
    EventEntity,
    RessourceEntity,
)
from skii.platform.models.agent import (
    TeacherAgent,
    StudentAgent,
)
from skii.platform.models.common import (
    VisualPicture,
    VisualAlbum,
    GeoCoordinate,
)


class Lesson(StateEntity, EventEntity):
    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lesson(s)")
        ordering = ["state", "-created", "-start", "-stop", "label"]
        constraints = [
            CheckConstraint(
                check=(
                    Q(start__lt=F("stop"))
                    & ~Q(  # Vérifie que start est inférieur à stop
                        start__range=(F("start"), F("stop"))
                    )
                    & ~Q(  # Vérifie qu'il n'y a pas de chevauchement
                        stop__range=(F("start"), F("stop"))
                    )  # Vérifie qu'il n'y a pas de chevauchement
                ),
                name="check_no_overlap",
            ),
        ]

    teacher = models.ForeignKey(TeacherAgent, on_delete=models.PROTECT)
    students = models.ManyToManyField(
        StudentAgent, blank=True, related_name="events_linked"
    )

    def __str__(self) -> str:
        start_datetime = self.start.strftime("%Y-%m-%d %H:%M")
        stop_datetime = self.stop.strftime("%Y-%m-%d %H:%M")
        return f"[{self.state}] {self.teacher.user.username}: {start_datetime} / {stop_datetime} "

    @property
    def gant_config(self):
        from skii.platform.schemas.vuejs import GanttConfigContract

        return GanttConfigContract(
            {
                "start": self.start.strftime(format="%Y-%m-%d %H:%M"),
                "stop": self.stop.strftime(format="%Y-%m-%d %H:%M"),
                "ganttBarConfig": {
                    "id": str(self.uuid),
                    "hasHandles": True,
                    "label": self.title,
                    "style": {
                        "background": "#e09b69",
                        "color": "black",
                        "borderRadius": "20px",
                    },
                },
            }
        )


class Location(RessourceEntity):
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
