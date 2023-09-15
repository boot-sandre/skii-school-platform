from typing import Optional

from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema

from skii.endpoint.schemas.ninja import IdentifierContract


class UserSchema(Schema):
    """Complete dj user schema generated from dj models

    Mostly to read records
    All technicals/Identifiant fields is excluded
    """
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]


class UserSaveSchema(ModelSchema):

    class Config:
        model = get_user_model()
        model_fields = ['username', 'first_name', 'last_name']


class StudentContract(IdentifierContract):
    user: UserSchema


class TeacherContract(IdentifierContract):
    user: UserSchema


class StudentSaveContract(IdentifierContract):
    user: UserSchema


class TeacherSaveContract(IdentifierContract):
    user: UserSchema

