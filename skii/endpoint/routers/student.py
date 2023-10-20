# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
""" Profile and user are related by foreign key.
"""
from typing import List

from django.db.models import Model
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from apps.base.schemas import FormInvalidResponseContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.platform.models.agent import StudentAgent
from skii.platform.schemas.agent import StudentContract, StudentSaveContract
from skii.endpoint.schemas.response import SkiiMsgContract

UserModel = get_user_model()


# Create a django ninja API router dedicated to the student
sub_route = Router(tags=["student"])


SubRouteModel: Model = StudentAgent
SubRouteContract = StudentContract
SubRouteSaveContract = StudentSaveContract


ListResponseContract = List[SubRouteContract]
ResponseContract = SubRouteContract


@sub_route.get(
    path="/list/",
    response={
        200: ListResponseContract,
        422: FormInvalidResponseContract,
    },
)
def list(request: HttpRequest):
    return 200, SubRouteModel.objects.all()


@sub_route.get(
    path="/fetch/{pk}/",
    response={
        200: ResponseContract,
        422: FormInvalidResponseContract,
    },
)
def fetch(request: HttpRequest, pk: IntStrUUID4):
    return 200, get_object_or_404(SubRouteModel, pk=pk)


@sub_route.delete(
    path="/delete/{pk}/",
    response={
        200: SkiiMsgContract,
        422: FormInvalidResponseContract,
    },
)
def delete(request: HttpRequest, pk: IntStrUUID4):
    qs = SubRouteModel.objects.all().filter(pk=pk)
    if qs.exists():
        qs.delete()
    return 200, SkiiMsgContract(message="OK")


@sub_route.post(
    path="/update/{pk}/",
    response={
        200: ResponseContract,
        422: FormInvalidResponseContract,
    },
)
def update(request: HttpRequest, pk: IntStrUUID4, payload: SubRouteSaveContract):
    record_payload = payload.dict()
    if "user" in record_payload:
        user_payload = record_payload["user"]
        user = UserModel.objects.get(pk=get_object_or_404(StudentAgent, pk=pk).user.pk)
        for attr, value in user_payload.items():
            setattr(user, attr, value)
        user.save()
        user.refresh_from_db()
        record_payload["user"] = user
    record = get_object_or_404(StudentAgent, pk=pk)
    for attr, value in record_payload.items():
        setattr(record, attr, value)
    record.save()
    record.refresh_from_db()
    return 200, record


@sub_route.post(
    path="/create/",
    response={
        200: ResponseContract,
        422: FormInvalidResponseContract,
    },
)
def create(request: HttpRequest, payload: SubRouteSaveContract):
    record_payload = payload.dict()
    user_payload = record_payload.pop("user")
    user_obj = UserModel(**user_payload)
    user_obj.save()
    record_payload["user"] = user_obj
    record = StudentAgent(**record_payload)
    record.save()
    record.refresh_from_db()
    return 200, record
