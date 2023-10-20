# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from ninja import ModelSchema

from skii.platform.entities import RecordIdentityHistory


class RecordIdentityHistotyContract(ModelSchema):
    class Config:
        model = RecordIdentityHistory
        model_fields = ["created", "last_modified"]
