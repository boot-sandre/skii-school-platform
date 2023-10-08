from typing import List, Type

from ninja import Schema, Field
from django.db.models import Model

from skii.platform.schemas.agent import TeacherContract
from skii.platform.schemas.event import LessonContract

SkiiRecordContract: Schema = Type[Model]
SkiiListContract: Schema = List[Model]


class SkiiMsgContract(Schema):
    message: str


class TeacherLessonContract(TeacherContract):
    """ Return Teachers agents with lessons related."""
    lessons: List[LessonContract] = Field(alias="lessonevent_set")


__all__ = [
    SkiiRecordContract,
    SkiiListContract,
    SkiiMsgContract,
    TeacherLessonContract,
]
