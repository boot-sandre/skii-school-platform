from datetime import datetime

from django.db.models import Q
from ninja import FilterSchema
from typing import Optional, TypeVarTuple, TypedDict


R = TypeVarTuple("R")


class RangeTimeLesson(TypedDict):
    start: datetime
    stop: datetime


class LessonFilterSchema(FilterSchema):
    """
    A schema for filtering lessons based on start and stop times.

    Attributes:
        start (Optional[datetime]): The minimum start time for filtering lessons.
        stop (Optional[datetime]): The maximum stop time for filtering lessons.

    Methods:
        custom_expression(): Generates a custom Q object for filtering based on the
                             provided start and stop times. Will be call instead of
                             using directly declared fields.
    """

    start: Optional[datetime] = None
    stop: Optional[datetime] = None

    def custom_expression(self) -> Q:
        """
        Generate a custom Q object for filtering lessons.

        Returns:
            Q: A Q object representing the custom filter expression based
            on start and stop times.
        """
        q_filter: Q = Q()
        if self.start:
            q_filter &= Q(
                start__gte=self.start
            )  # Filter for lessons starting greater than or equal to self.start
        if self.stop:
            q_filter &= Q(
                stop__lte=self.stop
            )  # Filter for lessons stopping less than or equal to self.stop
        return q_filter
