from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Schema

from skii.platform.schemas.vuejs import (
    GanttConfigContract,
)
from skii.platform.schemas.agent import (
    TeacherContract,
    StudentContract,
)


class LessonContract(Schema):
    gant_config: GanttConfigContract
    start: datetime
    stop: datetime
    teacher: TeacherContract
    students: List[StudentContract] = []
    uuid: Optional[UUID] = uuid4
