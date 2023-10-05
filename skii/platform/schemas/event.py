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
    TeacherSaveContract,
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
