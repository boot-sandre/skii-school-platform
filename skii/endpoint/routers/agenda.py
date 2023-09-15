from typing import Optional, List

from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.base.schemas import FormInvalidResponseContract

from skii.platform.schemas.agent import StudentContract, TeacherContract, UserSchema
from skii.platform.models.agent import TeacherAgent
from skii.platform.schemas.event import LessonContract
from skii.endpoint.schemas.ninja import SkiiListContract

UserModel = get_user_model()


route_agenda = Router(tags=["skii", "agenda"])


class TeacherLessonContract(TeacherContract):
    user: UserSchema
    id: Optional[int]
    lessons: List[LessonContract] = []


@route_agenda.post(
    path="/fetch_teacher_agenda/{record_pk}/",
    response={
        200: SkiiListContract,
        422: FormInvalidResponseContract,
    },
)
def fetch_teacher_agenda(
    request: HttpRequest, record_pk: int, payload: StudentContract
):
    agent_payload = payload.dict()
    user_payload = agent_payload.pop("user")
    agent_obj = get_object_or_404(TeacherAgent, id=record_pk)
    user_obj = get_object_or_404(UserModel, id=agent_obj.user.id)
    for attr, value in agent_payload.items():
        setattr(agent_obj, attr, value)
    agent_obj.save()
    for attr, value in user_payload.items():
        setattr(user_obj, attr, value)
    user_obj.save()
    agent_obj.refresh_from_db()
    agent_obj.user.refresh_from_db()
    return dict(
        count=int(bool(agent_obj)),
        item=agent_obj,
    )
