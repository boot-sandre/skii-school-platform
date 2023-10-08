from datetime import datetime, timedelta

from ninja import FilterSchema, Field
from typing import Optional, TypeVar, TypeVarTuple, TypedDict


R = TypeVarTuple("R")


class RangeTimeLesson(TypedDict):
    start: datetime
    stop: datetime


class LessonFilterSchema(FilterSchema):
    # time_range: R[datetime, datetime] = (datetime.now(), datetime.now() + timedelta(hours=12))
    # time_range: RangeTimeLesson = dict(start=datetime.now(), stop=datetime.now() + timedelta(hours=12))
    start: Optional[datetime] = None
    stop: Optional[datetime] = None
