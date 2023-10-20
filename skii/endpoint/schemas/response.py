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
