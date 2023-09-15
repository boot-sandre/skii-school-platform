from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.base.schemas import FormInvalidResponseContract

from skii.platform.models.agent import TeacherAgent
from skii.platform.models.event import Lesson
from skii.platform.interfaces import AgendaInterface
from skii.platform.schemas.event import LessonContract
from skii.endpoint.schemas.ninja import SkiiRecordContract, SkiiListContract

UserModel = get_user_model()


# Create a django ninja API router dedicated to the skii platform
route_lesson = Router(tags=["skii", "event", "lesson"])


@route_lesson.get(
    path="/fetch/{record_pk}/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def lesson_record(request: HttpRequest, record_pk: int | str):
    obj = get_object_or_404(Lesson, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        data=obj,
    )


@route_lesson.get(
    path="/lesson_list_by_teacher/{teacher_pk}/",
    response={
        200: SkiiListContract,
        422: FormInvalidResponseContract,
    },
)
def teacher_lesson_list(request: HttpRequest, teacher_pk: int):
    lesson_list = AgendaInterface.list_teacher_lesson(
        agent=TeacherAgent.objects.get(pk=teacher_pk)
    )
    return dict(
        items=list(lesson_list),
        count=lesson_list.count(),
    )


@route_lesson.get(
    path="/list/",
    response={
        200: SkiiListContract,
        422: FormInvalidResponseContract,
    },
)
def lesson_record_list(request: HttpRequest):
    qs = Lesson.objects.all()
    return dict(
        items=list(qs),
        count=qs.count(),
    )


@route_lesson.delete(
    path="/delete/{record_id}/",
)
def record_delete(request: HttpRequest, record_id: int | str):
    qs = Lesson.objects.all().get(pk=record_id)
    qs.delete()
    return dict(
        message="Success",
    )


@route_lesson.post(
    path="/save/{record_id}/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def record_save(
    request: HttpRequest, record_id: int | str, payload: LessonContract
):
    lesson_payload = payload.dict()
    lesson_obj = get_object_or_404(Lesson, pk=record_id)
    for attr, value in lesson_payload.items():
        setattr(lesson_obj, attr, value)
    lesson_obj.save()
    lesson_obj.refresh_from_db()
    return dict(
        count=int(bool(lesson_obj)),
        data=lesson_obj,
    )


@route_lesson.post(
    path="/create/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def record_create(request: HttpRequest, payload: LessonContract):
    record_payload = payload.dict()
    record_obj = Lesson(**record_payload)
    record_obj.save()
    return dict(
        count=int(bool(record_obj)),
        item=record_obj,
    )
