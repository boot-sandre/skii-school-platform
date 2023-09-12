from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from skii.plateform.models import StudentAgent
from skii.skii_school_api.schemas import (
    StudentContract,
    StudentContractShort,
)


UserModel = get_user_model()


# Create a django ninja API router dedicated to the skii plateform platform
route_student = Router(tags=["skii", "student"])


@route_student.get(
    path="/fetch/{record_pk}/",
    response={
        200: StudentRecordResponse,
        422: FormErrorsResponseContract,
    },
)
def student_record(request: HttpRequest, record_pk: int):
    obj = get_object_or_404(StudentAgent, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        model=f"{StudentAgent.Meta.verbose_name}",
        item=obj,
    )


@route_student.get(
    path="/list/",
    response={
        200: StudentListResponse,
        422: FormErrorsResponseContract,
    },
)
def student_record_list(request: HttpRequest):
    qs = StudentAgent.objects.all()
    agent_count = qs.count()
    return dict(
        items=list(qs), count=agent_count, model=f"{StudentAgent.Meta.verbose_name}"
    )


@route_student.delete(
    path="/delete/{record_id}/",
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
        200: StudentRecordResponse,
        422: FormErrorsResponseContract,
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
        model=f"{StudentAgent.Meta.verbose_name}",
        item=agent_obj,
    )


@route_student.post(
    path="/create/",
    response={
        200: StudentRecordResponse,
        422: FormErrorsResponseContract,
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
        model=f"{StudentAgent.Meta.verbose_name}",
        item=agent_obj,
    )