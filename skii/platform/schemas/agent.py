# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import Optional

from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

from skii.endpoint.schemas.identifier import IntStrUUID4


class UserSchema(Schema):
    """DJ user schema used to read record."""

    pk: IntStrUUID4
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


class UserSaveSchema(ModelSchema):
    """DJ user schema used to save record."""

    class Config:
        model = get_user_model()
        model_fields = ["email", "username", "first_name", "last_name"]


class StudentContract(Schema):
    user: UserSchema
    pk: IntStrUUID4


class TeacherContract(Schema):
    user: UserSchema
    pk: IntStrUUID4


class StudentSaveContract(Schema):
    user: UserSaveSchema


class TeacherSaveContract(Schema):
    user: UserSaveSchema
