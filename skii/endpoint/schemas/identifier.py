# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import Type

from ninja.schema import Schema
from pydantic import UUID4


IntStrUUID4: Type = UUID4 | int | str


class IntStrUUID4Contract(Schema):
    pk: IntStrUUID4


__all__ = [
    IntStrUUID4Contract,
    IntStrUUID4,
]
