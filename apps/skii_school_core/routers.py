from ninja import Router
from ninja.security import django_auth
from packaging.version import parse as parse_version
from django.http import HttpResponse, HttpRequest
import json

# Get current package version
current_package_name = __package__.split(".")[0]
distrib_version = parse_version(__import__(current_package_name).__version__)


# Create a django ninja API router dedicated to the skii school platform
router = Router(tags=["api_skii_platform", "core"])


@router.get("/ping", auth=None)
def ping(request: HttpRequest):
    """A simple ping endpoint to check if the API is up and display api's version."""
    return HttpResponse(
        content=f"Welcome on Skii School Platform API: {distrib_version}\n{str(router.api.get_openapi_schema())}"
    )


@router.get("/info", auth=django_auth)
def info(request: HttpRequest):
    """A info endpoint to display api's parameters."""
    api_description = router.api.get_openapi_schema()
    return HttpResponse(
        content=json.dumps(api_description, indent=2), content_type="application/json"
    )
