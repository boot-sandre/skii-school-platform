# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from devtools import debug
from django.http import HttpRequest
from ninja import Schema


def devtools_debug(func):
    def wrapper(request: HttpRequest, payload: Schema):
        debug(request, payload)
        response = func(request, payload=payload)
        debug(response)
        return response

    return wrapper
