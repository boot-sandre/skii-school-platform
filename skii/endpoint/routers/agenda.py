from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from ninja import Router

from apps.base.schemas import FormInvalidResponseContract

from skii.platform.models.agent import TeacherAgent
from skii.endpoint.schemas.response import TeacherLessonContract
from skii.endpoint.schemas.identifier import IntStrUUID4


UserModel = get_user_model()


route_agenda = Router(tags=["skii", "agenda"])

RouterModel = TeacherAgent


@route_agenda.get(
    path="/teacher_lessons/{record_pk}/",
    response={
        200: TeacherLessonContract,
        422: FormInvalidResponseContract,
    },
)
def teacher_lessons(
    request: HttpRequest, record_pk: IntStrUUID4
):
    agent = get_object_or_404(RouterModel, pk=record_pk)
    return 200, agent
