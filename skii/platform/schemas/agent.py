from typing import Optional

from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

from skii.endpoint.schemas.identifier import IntStrUUID4


class UserSchema(Schema):
    """DJ user schema used to read record"""

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


class UserSaveSchema(ModelSchema):
    """DJ user schema used to save record"""

    class Config:
        model = get_user_model()
        model_fields = ["email", "username", "first_name", "last_name"]


class StudentContract(Schema):
    user: UserSchema


class TeacherContract(Schema):
    user: UserSchema


class StudentSaveContract(Schema):
    user: UserSaveSchema


class TeacherSaveContract(Schema):
    user: UserSaveSchema
