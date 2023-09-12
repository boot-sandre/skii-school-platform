from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.skii_school_core.models import TeacherAgent
from apps.skii_school_core.schemas import (
    FormErrorsResponseContract,
    StudentRecordResponse,
    TeacherListResponse,
    StudentContract,
    StudentContractShort,
)


UserModel = get_user_model()


route_agenda = Router(tags=["skii", "agenda"])


@route_agenda.post(
    path="/fetch_teacher_agenda/{record_pk}/",
    response={
        200: StudentRecordResponse,
        422: FormErrorsResponseContract,
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
        model=f"{TeacherAgent.Meta.verbose_name}",
        item=agent_obj,
    )
