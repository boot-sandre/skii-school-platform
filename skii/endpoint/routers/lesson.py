# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.base.schemas import FormInvalidResponseContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.endpoint.schemas.response import SkiiMsgContract
from skii.platform.models.event import LessonEvent
from skii.platform.schemas.event import LessonContract, LessonSaveContract


# Create a django ninja API router dedicated to the student
router = Router(tags=["lesson"])


RouterContract = LessonContract
RouterSaveContract = LessonSaveContract
RouterModel = LessonEvent
RouterListContract = List[RouterContract]


@router.post(
    path="/create/",
    response={
        200: RouterContract,
        422: FormInvalidResponseContract,
    },
)
def record_create(request: HttpRequest, payload: RouterSaveContract):
    record_payload = payload.dict()
    record = RouterModel(**record_payload)
    record.save()
    record.refresh_from_db()
    return 200, record


@router.get(
    path="/fetch/{pk}/",
    response={
        200: RouterContract,
        422: FormInvalidResponseContract,
    },
)
def record_read(request: HttpRequest, pk: IntStrUUID4):
    return 200, get_object_or_404(RouterModel, pk=pk)


@router.post(
    path="/update/{pk}/",
    response={
        200: RouterContract,
        422: FormInvalidResponseContract,
    },
)
def record_update(request: HttpRequest, pk: IntStrUUID4, payload: RouterSaveContract):
    record_payload = payload.dict()

    record = get_object_or_404(RouterModel, pk=pk)
    for attr, value in record_payload.items():
        setattr(record, attr, value)
    record.save()
    record.refresh_from_db()
    return 200, record


@router.delete(
    path="/delete/{pk}/",
    response={
        200: SkiiMsgContract,
        422: FormInvalidResponseContract,
    },
)
def record_delete(request: HttpRequest, pk: IntStrUUID4):
    qs = RouterModel.objects.all().filter(pk=pk)
    if qs.exists():
        qs.delete()
    return 200, SkiiMsgContract(message="OK")


@router.get(
    path="/list/",
    response={
        200: RouterListContract,
        422: FormInvalidResponseContract,
    },
)
def record_list(request: HttpRequest):
    return 200, RouterModel.objects.all()
