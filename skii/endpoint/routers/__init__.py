from .student import sub_route as route_student
from .teacher import sub_route as route_teacher
from .location import router as route_location
from .lesson import router as route_lesson
from .agenda import route_agenda

__all__ = [
    route_location,
    route_student,
    route_teacher,
    route_lesson,
    route_agenda,
]
