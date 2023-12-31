# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
import json
import logging
from ipaddress import IPv4Address, IPv6Address
from typing import Type, Mapping, Any, cast, List

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.datastructures import MultiValueDict
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import django_auth
from django.utils.translation import gettext_lazy as _
from ninja.types import DictStrAny
from pydantic import BaseModel

from skii.endpoint.routers import (
    route_student,
    route_teacher,
    route_location,
    route_lesson,
    route_agenda,
)

# Get current package version
from packaging.version import parse as parse_version


logger = logging.getLogger(__name__)


current_package_name = __package__.split(".")[0]
distrib_version = parse_version(__import__(current_package_name).__version__)


logger.info(f"Package: {current_package_name}")
logger.info(f"Distribution version: {distrib_version}")


class SkiiJSONEncoder(DjangoJSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.dict()
        if isinstance(o, (IPv4Address, IPv6Address)):
            return str(o)
        return super().default(o)


class SkiiJsonRenderer(BaseRenderer):
    media_type = "application/json"
    encoder_class: Type[json.JSONEncoder] = SkiiJSONEncoder
    json_dumps_params: Mapping[str, Any] = {}

    def render(self, request, data, *, response_status):
        return json.dumps(data, cls=self.encoder_class, **self.json_dumps_params)


class SkiiParser(Parser):
    def parse_body(self, request: HttpRequest) -> DictStrAny:
        return cast(DictStrAny, json.loads(request.body))

    def parse_querydict(
        self, data: MultiValueDict, list_fields: List[str], request: HttpRequest
    ) -> DictStrAny:
        result: DictStrAny = {}
        for key in data.keys():
            if key in list_fields:
                result[key] = data.getlist(key)
            else:
                result[key] = data[key]
        return result


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
    "renderer": SkiiJsonRenderer(),
    "parser": SkiiParser(),
}


def configure_api_skii() -> NinjaAPI:
    new_api = NinjaAPI(**api_kwargs)
    new_api.add_router(prefix="student", router=route_student)
    new_api.add_router(prefix="teacher", router=route_teacher)
    new_api.add_router(prefix="location", router=route_location)
    new_api.add_router(prefix="lesson", router=route_lesson)
    new_api.add_router(prefix="agenda", router=route_agenda)

    return new_api


# Create skii app dedicated api
api_skii: NinjaAPI = configure_api_skii()
logger.info(f"Api created: {api_skii.title}")
logger.info(f"Api version: {api_skii.version}")
logger.info(f"Api urlnamespace: {api_skii.urls_namespace}/")
logger.info(f"Api auth: {api_skii.auth}")
# logger.info(f"Api root path: {api_skii.root_path}")
logger.info(f"Api docs url: {api_skii.docs_url}")
logger.info(f"Api openapi url: {api_skii.openapi_url}")
logger.info(f"Api openapi extra: {api_skii.openapi_extra}")
logger.info(f"Api description: {api_skii.description}")


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
    return api_skii.create_response(request, data={"detail": exc.errors}, status=418)
