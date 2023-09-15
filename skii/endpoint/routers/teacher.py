from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from apps.base.schemas import FormInvalidResponseContract
from skii.platform.models.agent import TeacherAgent
from skii.platform.schemas.agent import TeacherContract, TeacherSaveContract
from skii.endpoint.schemas.ninja import SkiiMsgContract


UserModel = get_user_model()


# Create a django ninja API router dedicated to the teacher
sub_route = Router(tags=["skii", "agent", "teacher"])


SubRouteModel = TeacherAgent
SubRouteContract = TeacherContract
SubRouteSaveContract = TeacherSaveContract


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
def fetch(request: HttpRequest, pk: int | str):
    return 200, get_object_or_404(SubRouteModel, pk=pk)


@sub_route.delete(
    path="/delete/{pk}/",
    response={
        200: SkiiMsgContract,
        422: FormInvalidResponseContract,
    },
)
def delete(request: HttpRequest, pk: int | str):
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
def update(request: HttpRequest, pk: int | str, payload: SubRouteSaveContract):
    payload = payload.dict()
    user_payload = payload.pop("user")
    record = get_object_or_404(SubRouteModel, pk=pk)
    user_obj = get_object_or_404(UserModel, id=user_payload["id"])
    for attr, value in payload.items():
        setattr(record, attr, value)
    record.save()
    for attr, value in user_payload.items():
        setattr(user_obj, attr, value)
    user_obj.save()
    record.refresh_from_db()
    record.user.refresh_from_db()
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
    record = SubRouteModel(**record_payload)
    record.save()
    return 200, record
