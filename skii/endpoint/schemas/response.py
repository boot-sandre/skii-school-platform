# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import List, Type

from ninja import Schema
from django.db.models import Model

from skii.platform.schemas.agent import TeacherContract
from skii.platform.schemas.event import LessonContract

SkiiRecordContract: Schema = Type[Model]
SkiiListContract: Schema = List[Model]


class SkiiMsgContract(Schema):
    message: str


class TeacherLessonContract(TeacherContract):
    """Return Teachers agents with lessons related."""

    lessons_assigned: List[LessonContract]


class StudentLessonContract(TeacherContract):
    """Return Student agents with lessons related."""

    lessons_subscribed: List[LessonContract]


__all__ = [
    SkiiRecordContract,
    SkiiListContract,
    SkiiMsgContract,
    TeacherLessonContract,
    StudentLessonContract,
]
