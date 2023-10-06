from django.db import models
from django.db.models import F, Q, CheckConstraint

from django.utils.translation import gettext_lazy as _


from skii.platform.entities import (
    StateEntity,
    EventEntity,
)
from skii.platform.models.agent import (
    TeacherAgent,
    StudentAgent,
)


class LessonEvent(StateEntity, EventEntity):
    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lesson(s)")
        ordering = ["state", "-created", "-start", "-stop", "label"]
        constraints = [
            CheckConstraint(
                check=(Q(start__lt=F("stop"))),
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
            **{
                "startGant": self.start.strftime(format="%Y-%m-%d %H:%M"),
                "stopGant": self.stop.strftime(format="%Y-%m-%d %H:%M"),
                "ganttBarConfig": {
                    "id": str(self.short_prefix_guid),
                    "hasHandles": True,
                    "label": self.label,
                    "style": {
                        "background": "#e09b69",
                        "color": "black",
                        "borderRadius": "20px",
                    },
                },
            }
        )
