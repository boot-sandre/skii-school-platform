from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.base.schemas import FormInvalidResponseContract
from skii.platform.models.agent import TeacherAgent
from skii.platform.schemas.agent import (
    StudentContract,
    StudentContractShort,
)
from skii.platform.schemas.http import SkiiResponse, SkiiListResponse, MsgResponseContract


UserModel = get_user_model()


# Create a django ninja API router dedicated to the skii platform
route_teacher = Router(tags=["skii", "platform", "agent", "teacher"])


@route_teacher.get(
    path="/fetch/{record_pk}/",
    response={
        200: SkiiResponse,
        422: FormInvalidResponseContract,
    },
)
def fetch_record(request: HttpRequest, record_pk: int):
    obj = get_object_or_404(TeacherAgent, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        model=f"{obj._meta.model_name}",
        item=obj,
    )


@route_teacher.get(
    path="/list/",
    response={
        200: SkiiListResponse,
        422: FormInvalidResponseContract,
    },
)
def record_list(request: HttpRequest):
    agent_list = TeacherAgent.objects.all()
    agent_count = agent_list.count()
    return 200, dict(
        items=list(agent_list),
        count=agent_count,
        model=f"{agent_list.model._meta.model_name}",
    )


@route_teacher.delete(
    path="/delete/{record_pk}/",
)
def record_delete(request: HttpRequest, record_pk: int):
    qs = TeacherAgent.objects.all().get(pk=record_pk)
    qs.delete()
    return 200, dict(
        message="Success",
    )


@route_teacher.post(
    path="/save/{record_pk}/",
    response={
        200: SkiiResponse,
        422: FormInvalidResponseContract,
    },
)
def record_save(request: HttpRequest, record_pk: int, payload: StudentContract):
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


@route_teacher.post(
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
    agent_obj = TeacherAgent(**agent_payload)
    agent_obj.save()
    return dict(
        count=int(bool(agent_obj)),
        model=f"{TeacherAgent.Meta.verbose_name}",
        item=agent_obj,
    )
