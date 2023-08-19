from ninja import Schema, ModelSchema
from django.contrib.auth import get_user_model
from typing import Dict, List, Any

from apps.skii_school_core.models import StudentAgent, TeacherAgent

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
    class Config:
        model = User
        model_fields = "__all__"
        model_exclude = [
            "password", "is_superuser", "is_staff",
            "groups", "user_permissions",
            "date_joined", "last_login"
        ]
        model_optional_fields = ["id"]


class StudentContract(ModelSchema):
    user: UserSchema

    class Config:
        model = StudentAgent
        model_fields = "__all__"
        model_exclude = ["id", "last_modified", "created"]


class StudentContractShort(ModelSchema):
    user: UserSchemaShort

    class Config:
        model = StudentAgent
        model_fields = ["user", "id"]
        model_optional_fields = ["id"]


class StudentRecordResponse(Schema):
    model: str
    count: int
    item: StudentContractShort | None


class StudentListResponse(Schema):
    model: str
    count: int
    items: List[StudentContractShort] = []


class TeacherContract(ModelSchema):
    user: UserSchema

    class Config:
        model = TeacherAgent
        model_fields = "__all__"
        model_exclude = ["id"]


class TeacherContractShort(ModelSchema):
    user: UserSchemaShort

    class Config:
        model = TeacherAgent
        model_fields = ["user"]
        model_optional_fields = ["id"]


class TeacherRecordResponse(Schema):
    model: str
    count: int
    item: TeacherContractShort | None


class TeacherListResponse(Schema):
    model: str
    count: int
    items: List[TeacherContractShort] = []
