import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import django_auth
from django.utils.translation import gettext_lazy as _

from skii.skii_school_api.routers import (
    route_student,
    route_teacher,
    route_location,
    route_lesson,
    route_agenda,
)

# Get current package version
from packaging.version import parse as parse_version


current_package_name = __package__.split(".")[0]
distrib_version = parse_version(__import__(current_package_name).__version__)


api_kwargs = {
    "title": _("Skii School Platform"),
    "version": distrib_version.base_version,
    "description": _(
        _("Web application to put in relation skii teacher with skii student")
    ),
    "auth": django_auth,
    "csrf": True,
    "docs_decorator": staff_member_required,
    "urls_namespace": "skii",
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
    print(json.dumps(exc.errors, indent=2))
    return api_skii.create_response(request, data={"detail": exc.errors}, status=418)


api_skii.add_router(prefix="student", router=route_student)
api_skii.add_router(prefix="teacher", router=route_teacher)
api_skii.add_router(prefix="location", router=route_location)
api_skii.add_router(prefix="lesson", router=route_lesson)
api_skii.add_router(prefix="agenda", router=route_agenda)
