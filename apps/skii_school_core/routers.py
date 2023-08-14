from django.shortcuts import get_object_or_404
from ninja import Router
from django.http import HttpResponse, HttpRequest
import json

from apps.skii_school_core.models import StudentAgent
from apps.skii_school_core.schemas import (
    FormErrorsResponseContract,
    StudentListResponse,
    StudentSingleResponse,
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
        200: StudentListResponse,
        422: FormErrorsResponseContract,
    },
)
def agent_list(request: HttpRequest):
    qs = StudentAgent.objects.all()
    agent_count = qs.count()
    return dict(
        status=200,
        data=dict(
            items=list(qs), count=agent_count, model=f"{StudentAgent.Meta.verbose_name}"
        ),
    )


@route_skii.get(
    path="student/{student_id}",
    response={
        200: StudentSingleResponse,
        422: FormErrorsResponseContract,
    },
)
def agent_single(request: HttpRequest, student_id: int):
    obj = get_object_or_404(StudentAgent, pk=student_id)
    return dict(
        status=200,
        data=dict(
            item=obj, count=int(bool(obj)), model=f"{StudentAgent.Meta.verbose_name}"
        ),
    )
