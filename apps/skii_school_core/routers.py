from ninja import Router
from django.http import HttpResponse, HttpRequest
import json

# from apps.skii_school_core.api import api_skii
from apps.skii_school_core.models import StudentAgent
from apps.skii_school_core.schemas import (
    DataResponseContract,
    FormErrorsResponseContract,
    StudentListContract,
)


# Create a django ninja API router dedicated to the skii school platform
route_skii = Router(tags=["api_skii_platform"])


@route_skii.get(path="/info")
def info(request: HttpRequest):
    """Info endpoint to display api's parameters."""
    api_description = route_skii.api.get_openapi_schema()
    return HttpResponse(
        content=json.dumps(api_description, indent=2), content_type="application/json"
    )


@route_skii.get(
    path="student/list",
    response={
        200: StudentListContract,
        422: FormErrorsResponseContract,
    },
)
def get(request: HttpRequest):
    qs = StudentAgent.objects.all()
    return {"status": 200, "data": dict(items=qs.values_list(), count=qs.count())}


@route_skii.get(
    path="student/{student_id}",
    response={
        200: DataResponseContract,
        422: FormErrorsResponseContract,
    },
)
def get(request: HttpRequest, student_id: int):
    breakpoint()
    qs = StudentAgent.objects.all()
    return dict(status=200, data=qs.get(pk=student_id))
