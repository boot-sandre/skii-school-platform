import orjson
from ninja.renderers import BaseRenderer
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import django_auth
from django.utils.translation import gettext_lazy as _

from skii.endpoint.routers.student import route_student
from skii.endpoint.routers.teacher import route_teacher
from skii.endpoint.routers.location import route_location
from skii.endpoint.routers.lesson import route_lesson
from skii.endpoint.routers.agenda import route_agenda

# Get current package version
from packaging.version import parse as parse_version


current_package_name = __package__.split(".")[0]
distrib_version = parse_version(__import__(current_package_name).__version__)



class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


api_kwargs = {
    "title": _("Skii Platform"),
    "version": distrib_version.base_version,
    "description": _(
        _("Web application to put in relation skii teacher with skii student")
    ),
    "auth": django_auth,
    "csrf": True,
    "docs_decorator": staff_member_required,
    "urls_namespace": "skii",
    "renderer": ORJSONRenderer(),
}

# Create skii app dedicated api
api_skii = NinjaAPI(**api_kwargs)


@api_skii.exception_handler(ValidationError)
def custom_validation_errors(
    request: HttpRequest, exc: ValidationError
) -> HttpResponse:
    """A validator that will fire a 418 and a message \
    if the data is not compliant to the endpoint schema

    Args:
        request (HttpRequest): the Django http request
        exc (Exception): an exception

    Returns:
        HttpResponse: a Django http response
    """
    breakpoint()
    return api_skii.create_response(request, data={"detail": exc.errors}, status=418)


api_skii.add_router(prefix="student", router=route_student)
api_skii.add_router(prefix="teacher", router=route_teacher)
api_skii.add_router(prefix="location", router=route_location)
api_skii.add_router(prefix="lesson", router=route_lesson)
api_skii.add_router(prefix="agenda", router=route_agenda)
