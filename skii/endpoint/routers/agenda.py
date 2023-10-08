from django.http import HttpRequest
from django.contrib.auth import get_user_model

from ninja import Router, Query

from apps.base.schemas import FormInvalidResponseContract
from skii.endpoint.filters import LessonFilterSchema

from skii.platform.models.agent import TeacherAgent
from skii.endpoint.schemas.response import TeacherLessonContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.platform.models.event import LessonEvent

UserModel = get_user_model()


route_agenda = Router(tags=["skii", "agenda"])

RouterModel = LessonEvent


@route_agenda.get(
    path="/teacher_lessons/{teacher_pk}/",
    response={
        200: TeacherLessonContract,
        422: FormInvalidResponseContract,
    },
)
def teacher_lessons(
    request: HttpRequest,
    teacher_pk: IntStrUUID4,
    filters: LessonFilterSchema = Query(...),
):
    lessons = LessonEvent.objects.all()
    lessons = filters.filter(lessons)
    agent = TeacherAgent.objects.get(pk=teacher_pk)
    setattr(agent, "lessons", lessons)
    return 200, agent
