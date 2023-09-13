from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from apps.base.schemas import FormInvalidResponseContract
from skii.platform.models.agent import StudentAgent
from skii.platform.schemas.agent import (
    StudentContract,
    StudentContractShort,
)
from skii.platform.schemas.http import (
    SkiiListResponse,
    SkiiResponse,
    MsgResponseContract,
)

UserModel = get_user_model()


# Create a django ninja API router dedicated to the skii platform
route_student = Router(tags=["skii", "platform", "agent", "student"])


@route_student.get(
    path="/record_get/{record_pk}/",
    response={
        200: SkiiResponse,
        422: FormInvalidResponseContract,
    },
)
def record_get(request: HttpRequest, record_pk: int):
    obj = get_object_or_404(StudentAgent, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        data=obj,
    )


@route_student.get(
    path="/record_list/",
    response={
        200: SkiiListResponse,
        422: FormInvalidResponseContract,
    },
)
def record_list(request: HttpRequest):
    qs = StudentAgent.objects.all()
    agent_count = qs.count()
    return dict(
        data=list(qs), count=agent_count
    )


@route_student.delete(
    path="/record_delete/{record_id}/",
    response={
        200: MsgResponseContract,
    },
)
def record_delete(request: HttpRequest, record_id: int):
    qs = StudentAgent.objects.all().get(pk=record_id)
    qs.delete()
    return dict(
        message="Success",
    )


@route_student.post(
    path="/save/{record_id}/",
    response={
        200: SkiiListResponse,
        422: FormInvalidResponseContract,
    },
)
def record_save(request: HttpRequest, record_id: int, payload: StudentContract):
    agent_payload = payload.dict()
    user_payload = agent_payload.pop("user")
    agent_obj = get_object_or_404(StudentAgent, id=record_id)
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
        data=agent_obj,
    )


@route_student.post(
    path="/create/",
    response={
        200: SkiiResponse,
        422: FormInvalidResponseContract,
    },
)
def record_create(request: HttpRequest, payload: StudentContractShort):
    agent_payload = payload.dict()
    user_payload = agent_payload.pop("user")
    user_obj = UserModel(**user_payload)
    user_obj.save()
    agent_payload["user"] = user_obj
    agent_obj = StudentAgent(**agent_payload)
    agent_obj.save()
    return dict(
        count=int(bool(agent_obj)),
        data=agent_obj,
    )
