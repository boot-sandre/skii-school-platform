import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import django_auth


from .routers import router as skii_school_core_router
from .routers import distrib_version as __version__


api_kwargs = {
    "title": "Skii School Platform Core apps",
    "version": __version__.base_version,
    "description": "Web application to put in relation skii teacher with skii student",
    "auth": django_auth,
    "csrf": True,
    "docs_decorator": staff_member_required,
    "urls_namespace": "skii-school-platform",
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
    return api_skii.create_response(request, {"detail": exc.errors}, status=418)


api_skii.add_router("/core/", skii_school_core_router)
