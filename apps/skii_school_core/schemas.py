from ninja import Schema, ModelSchema
from django.contrib.auth import get_user_model
from typing import Dict, List, Any

from apps.skii_school_core.models import (
    StudentAgent,
    TeacherAgent,
    Location,
    GeoCoordinate,
    Event,
)

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
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "id",
        ]


class UserSchemaShort(ModelSchema):
    class Config:
        model = User
        model_fields = "__all__"
        model_exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "date_joined",
            "last_login",
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


class CountryContract(Schema):
    code: str
    name: str
    flag: str


class VisualPictureContract(Schema):
    picture_url: str
    title: str


class GeoCoordinateContract(ModelSchema):
    class Config:
        model = GeoCoordinate
        model_fields = ["latitude", "longitude"]


class LocationContract(ModelSchema):
    country: CountryContract
    cover: VisualPictureContract | None
    coordinate: GeoCoordinateContract | None

    class Config:
        model = Location
        model_fields = "__all__"
        model_exclude = ["country", "cover", "coordinate"]


class LocationContractShort(ModelSchema):
    country: str

    class Config:
        model = Location
        model_fields = "__all__"
        model_exclude = ["last_modified", "created", "country"]


class LocationRecordResponse(Schema):
    model: str
    count: int
    item: LocationContract | None


class LocationListResponse(Schema):
    model: str
    count: int
    items: List[LocationContract] = []


class EventContract(ModelSchema):
    class Config:
        model = Event
        model_fields = "__all__"
        model_exclude = ["last_modified", "created"]


class EventListResponse(Schema):
    model: str
    count: int
    items: List[EventContract] = []


class EventRecordResponse(LocationRecordResponse):
    item: EventContract | None


class EventContractShort(ModelSchema):
    class Config:
        model = Location
        model_fields = "__all__"
        model_exclude = ["last_modified", "created"]

