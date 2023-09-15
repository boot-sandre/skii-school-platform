from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.base.schemas import FormInvalidResponseContract
from skii.platform.models.agent import StudentAgent
from skii.platform.schemas.agent import (
    StudentContract, StudentSaveContract
)
from skii.endpoint.schemas.ninja import SkiiRecordContract, SkiiListContract, SkiiMsgContract


UserModel = get_user_model()


# Create a django ninja API router dedicated to the student
sub_route = Router(tags=["skii", "agent", "student"])


SubRouteModel = StudentAgent
SubRouteContract = StudentContract
SubRouteSaveContract = StudentSaveContract


class RecordContract(SkiiRecordContract):
    data = SubRouteContract


class ListContract(SkiiListContract):
    data: List[SubRouteContract] = []


@sub_route.get(
    path="/list/",
    response={
        200: ListContract,
        422: FormInvalidResponseContract,
    },
)
def list(request: HttpRequest):
    record_list = SubRouteModel.objects.all()
    return 200, dict(data=record_list)


@sub_route.get(
    path="/fetch/{pk}/",
    response={
        200: RecordContract,
        422: FormInvalidResponseContract,
    },
)
def fetch(request: HttpRequest, pk: int | str):
    record = get_object_or_404(SubRouteModel, pk=pk)
    return 200, dict(data=record)



@sub_route.delete(
    path="/delete/{pk}/",
    response={
        200: SkiiMsgContract,
        422: FormInvalidResponseContract,
    },
)
def delete(request: HttpRequest, pk: int | str):
    qs = SubRouteModel.objects.all().get(pk=pk)
    if qs.exist():
        qs.delete()
    return 200, dict(message="OK")


@sub_route.post(
    path="/save/{pk}/",
    response={
        200: RecordContract,
        422: FormInvalidResponseContract,
    },
)
def save(request: HttpRequest, pk: int | str, payload: SubRouteContract):
    record_payload = payload.dict()
    user_payload = record_payload.pop("user")
    record_obj = get_object_or_404(SubRouteModel, id=pk)
    user_obj = get_object_or_404(UserModel, id=user_payload["pk"])
    for attr, value in record_payload.items():
        setattr(record_obj, attr, value)
    record_obj.save()
    for attr, value in user_payload.items():
        setattr(user_obj, attr, value)
    user_obj.save()
    record_obj.refresh_from_db()
    record_obj.user.refresh_from_db()
    return 200, dict(data=record_obj)


@sub_route.post(
    path="/create/",
    response={
        200: RecordContract,
        422: FormInvalidResponseContract,
    },
)
def create(request: HttpRequest, payload: SubRouteContract):
    record_payload = payload.dict()
    user_payload = record_payload.pop("user")
    user_obj = UserModel(**user_payload)
    user_obj.save()
    record_payload["user"] = user_obj
    record = SubRouteModel(**record_payload)
    record.save()
    return 200, dict(data=record)
