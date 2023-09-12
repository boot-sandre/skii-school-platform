from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.skii_school_core.models import Lesson, TeacherAgent
from apps.skii_school_core.schemas import (
    LessonContract,
)
from apps.skii_school_core.interfaces import AgendaInterface


UserModel = get_user_model()


# Create a django ninja API router dedicated to the skii school platform
route_lesson = Router(tags=["skii", "lesson"])


@route_lesson.get(
    path="/fetch/{record_pk}/",
    response={
        200: EventRecordResponse,
        422: FormErrorsResponseContract,
    },
)
def lesson_record(request: HttpRequest, record_pk: int | str):
    obj = get_object_or_404(Lesson, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        model=f"{obj._meta.model_name}",
        item=obj,
    )


@route_lesson.get(
    path="/lesson_list_by_teacher/{teacher_pk}/",
    response={
        200: EventListResponse,
        422: FormErrorsResponseContract,
    },
)
def lesson_list_by_teacher(request: HttpRequest, teacher_pk: int):
    lesson_list = AgendaInterface.list_teacher_lesson(
        agent=TeacherAgent.objects.get(pk=teacher_pk)
    )
    return dict(
        items=list(lesson_list),
        count=lesson_list.count(),
        model=f"{lesson_list.model._meta.model_name}",
    )


@route_lesson.get(
    path="/list/",
    response={
        200: EventListResponse,
        422: FormErrorsResponseContract,
    },
)
def lesson_record_list(request: HttpRequest):
    qs = Event.objects.all()
    return dict(
        items=list(qs),
        count=qs.count(),
        model=f"{qs.model._meta.model_name}",
    )


@route_lesson.delete(
    path="/delete/{record_id}/",
)
def record_delete(request: HttpRequest, record_id: int | str):
    qs = Event.objects.all().get(pk=record_id)
    qs.delete()
    return dict(
        message="Success",
    )


@route_lesson.post(
    path="/save/{record_id}/",
    response={
        200: EventRecordResponse,
        422: FormErrorsResponseContract,
    },
)
def record_save(
    request: HttpRequest, record_id: int | str, payload: LessonContractShort
):
    location_payload = payload.dict()
    location_obj = get_object_or_404(Event, pk=record_id)
    for attr, value in location_payload.items():
        setattr(location_obj, attr, value)
    location_obj.save()
    location_obj.refresh_from_db()
    return dict(
        count=int(bool(location_obj)),
        model=f"{location_obj._meta.model_name}",
        item=location_obj,
    )


@route_lesson.post(
    path="/create/",
    response={
        200: EventRecordResponse,
        422: FormErrorsResponseContract,
    },
)
def record_create(request: HttpRequest, payload: LessonContractShort):
    record_payload = payload.dict()
    record_obj = Event(**record_payload)
    record_obj.save()
    return dict(
        count=int(bool(record_obj)),
        model=f"{record_obj._meta.verbose_name}",
        item=record_obj,
    )
