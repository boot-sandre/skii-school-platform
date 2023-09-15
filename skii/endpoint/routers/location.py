from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpRequest

from apps.base.schemas import FormInvalidResponseContract
from skii.platform.models.event import Location
from skii.platform.schemas.event import LocationContract
from skii.endpoint.schemas.ninja import SkiiRecordContract, SkiiListContract

route_location = Router(tags=["skii", "location"])


@route_location.get(
    path="/fetch/{record_pk}/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def location_record(request: HttpRequest, record_pk: int | str):
    obj = get_object_or_404(Location, pk=record_pk)
    return dict(
        count=int(bool(obj)),
        item=obj,
    )


@route_location.get(
    path="/list/",
    response={
        200: SkiiListContract,
        422: FormInvalidResponseContract,
    },
)
def location_record_list(request: HttpRequest):
    qs = Location.objects.all()
    return dict(
        data=list(qs),
        count=qs.count(),
    )


@route_location.delete(
    path="/delete/{record_id}/",
)
def record_delete(request: HttpRequest, record_id: int | str):
    qs = Location.objects.all().get(pk=record_id)
    qs.delete()
    return dict(
        message="Success",
    )


@route_location.post(
    path="/save/{record_id}/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def record_save(request: HttpRequest, record_id: int | str, payload: LocationContract):
    location_payload = payload.dict()
    location_obj = get_object_or_404(Location, pk=record_id)
    for attr, value in location_payload.items():
        setattr(location_obj, attr, value)
    location_obj.save()
    location_obj.refresh_from_db()
    return dict(
        count=int(bool(location_obj)),
        model=f"{location_obj._meta.model_name}",
        item=location_obj,
    )


@route_location.post(
    path="/create/",
    response={
        200: SkiiRecordContract,
        422: FormInvalidResponseContract,
    },
)
def record_create(request: HttpRequest, payload: LocationContract):
    record_payload = payload.dict()
    record_obj = Location(**record_payload)
    record_obj.save()
    return dict(
        count=int(bool(record_obj)),
        model=f"{record_obj._meta.verbose_name}",
        item=record_obj,
    )
