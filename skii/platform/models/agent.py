# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from skii.platform.entities import (
    AgentEntity,
)


class StudentAgent(AgentEntity):
    """Student needs to be related to an active user."""

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Student(s)")
        ordering = ["-last_modified", "-created", "user__username"]


class TeacherAgent(AgentEntity):
    """Teacher needs to be related to a staff user."""

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={"is_active": True, "is_staff": True},
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teacher(s)")
        ordering = ["-last_modified", "-created", "user__username"]
