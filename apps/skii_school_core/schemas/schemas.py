from datetime import datetime
from uuid import UUID

from ninja import Schema
from django.contrib.auth import get_user_model
from typing import List

from apps.skii_school_core.models.agent import (
    TeacherContract,
    StudentContract,
)
from apps.skii_school_core.schemas import GanttConfigContract

User = get_user_model()


# """""""""
# " Agent "
# """""""""


class CountryContract(Schema):
    code: str
    name: str
    flag: str


class VisualPictureContract(Schema):
    picture_url: str
    title: str


class LessonContract(Schema):
    gant_config: GanttConfigContract
    start: datetime
    stop: datetime
    teacher: TeacherContract
    students: List[StudentContract]
    uuid: UUID
