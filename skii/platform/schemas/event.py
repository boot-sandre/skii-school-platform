# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from datetime import datetime
from typing import List
from skii.endpoint.schemas.identifier import IntStrUUID4

from ninja import Schema

from skii.platform.schemas.vuejs import (
    GanttConfigContract,
)
from skii.platform.schemas.agent import (
    TeacherContract,
    StudentContract,
)


class LessonContract(Schema):
    pk: IntStrUUID4
    gant_config: GanttConfigContract
    start: datetime
    stop: datetime
    teacher: TeacherContract
    students: List[StudentContract] = []
    label: str
    description: str


class LessonSaveContract(Schema):
    label: str
    description: str
    start: datetime
    stop: datetime
    teacher_id: int
