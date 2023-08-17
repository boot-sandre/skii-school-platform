from ninja import Schema, ModelSchema
from apps.skii_school_core.entities import (
    AgentEntity,
)
from django.contrib.auth import get_user_model
from typing import Dict, List, Any, Union

from apps.skii_school_core.models import StudentAgent

User = get_user_model()


class MessageResponseContract(Schema):
    message: str


class FormErrorsResponseContract(Schema):
    errors: Dict[str, List[Dict[str, Any]]]


class IdContract(Schema):
    id: int


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = "__all__"
        model_exclude = [
            "password", "is_superuser", "is_staff",
            "groups", "user_permissions",
            "id"
        ]


class UserSchemaShort(ModelSchema):
    id: int
    class Config(UserSchema.Config):
        model = User
        model_fields = "__all__"
        model_exclude = [
            "password", "is_superuser", "is_staff",
            "groups", "user_permissions",
            "date_joined", "last_login"
        ]


class StudentContract(ModelSchema):
    user: UserSchema

    class Config:
        model = StudentAgent
        model_fields = "__all__"
        model_exclude = ["id"]


class StudentContractShort(ModelSchema):
    user: UserSchemaShort
    id: int

    class Config:
        model = StudentAgent
        model_fields = ["user", "id"]


class StudentRecordResponse(Schema):
    model: str
    count: int
    item: StudentContract | None


class StudentListResponse(Schema):
    model: str
    count: int
    items: List[StudentContractShort] = []
