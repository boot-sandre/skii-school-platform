from typing import List

from django.db.models import Model

from skii.endpoint.routers.abstract import RestRouterProducer
from skii.platform.models.event import Lesson


class AutomatedLessonRouter(RestRouterProducer):
    class Config(RestRouterProducer.Config):
        model: Model = Lesson
        name: str = "lesson"
        operation: List[str] = ["create", "read", "update", "delete", "list"]
        tags = ["lesson"]


LessonEventRouter = AutomatedLessonRouter()

__all__ = [
    LessonEventRouter
]
