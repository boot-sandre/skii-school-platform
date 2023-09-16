from .student import sub_route as route_student
from .teacher import sub_route as route_teacher

from .location import LocationResourceRouter
from .lesson import LessonEventRouter

__all__ = [
    LocationResourceRouter,
    LessonEventRouter,
]
