from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.base.schemas import FormInvalidResponseContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.endpoint.schemas.response import SkiiMsgContract
from skii.platform.models.common import GeoCoordinate
from skii.platform.models.resource import LocationResource
from skii.platform.schemas.resource import LocationContract, LocationSaveContract


# Create a django ninja API router dedicated to the student
router = Router(tags=["location"])


RouterContract = LocationContract
RouterSaveContract = LocationSaveContract
RouterModel = LocationResource
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
    if "coordinate" in record_payload:
        geo_coordinate = record_payload["coordinate"]
        del record_payload["coordinate"]
        geo_coordinate_obj, created = GeoCoordinate.objects.update_or_create(
            geo_coordinate, **geo_coordinate
        )
        record_payload["coordinate"] = geo_coordinate_obj
    record = RouterModel(**record_payload)
    record.save()
    record.refresh_from_db()
    return 200, record


@router.get(
    path="/read/{pk}/",
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
    if "coordinate" in record_payload:
        geo_coordinate = record_payload["coordinate"]
        del record_payload["coordinate"]
        geo_coordinate_obj, created = GeoCoordinate.objects.update_or_create(
            geo_coordinate, **geo_coordinate
        )
        record_payload["coordinate"] = geo_coordinate_obj
    record = get_object_or_404(RouterModel, pk=pk)
    for attr, value in record_payload.items():
        setattr(record, attr, value)
    record.save()
    record.refresh_from_db()
    return 200, record


@router.get(
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
    return 200, SkiiMsgContract(message="Record deleted")


@router.get(
    path="/list/",
    response={
        200: RouterListContract,
        422: FormInvalidResponseContract,
    },
)
def record_list(request: HttpRequest):
    return 200, RouterModel.objects.all()


__all__ = [router]
