from django.utils.translation import gettext_lazy as _

from skii.platform.entities import (
    AgentEntity,
)


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
