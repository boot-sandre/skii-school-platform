from datetime import datetime

from django.db.models import Q
from ninja import FilterSchema
from typing import Optional, TypeVarTuple, TypedDict


R = TypeVarTuple("R")


class RangeTimeLesson(TypedDict):
    start: datetime
    stop: datetime


class LessonFilterSchema(FilterSchema):
    # time_range: R[datetime, datetime] = (
    #         datetime.now(), datetime.now() + timedelta(hours=12))
    # time_range: RangeTimeLesson = dict(
    #         start=datetime.now(), stop=datetime.now() + timedelta(hours=12))
    start: Optional[datetime] = None
    stop: Optional[datetime] = None

    def custom_expression(self) -> Q:
        q_filter: Q = Q()
        if self.start:
            q_filter &= Q(start__gt=self.start)
        if self.stop:
            q_filter &= Q(stop__lt=self.stop)
        return q_filter
