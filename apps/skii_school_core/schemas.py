from ninja import Schema, ModelSchema
from apps.skii_school_core.entities import (
    AgentEntity,
)
from django.contrib.auth import get_user_model
from typing import Dict, List, Any, Union


User = get_user_model()


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = "__all__"


class MessageResponseContract(Schema):
    status: int
    message: str


class DataResponseContract(Schema):
    status: int
    data: Union[Dict, List]


class FormErrorsResponseContract(Schema):
    errors: Dict[str, List[Dict[str, Any]]]


class Country(Schema):
    name: str
    value: str
    flag: str


#
# class DisplayContract(ModelSchema):
#     class Config:
#         model = DisplayEntity
#         model_fields = ["label"]
#         model_fields_optional = ["description"]

#
# class DescriptionContract(ModelSchema):
#     class Config:
#         model = DescriptionEntity
#         model_fields = []
#         model_fields_optional = ["description_short"]


class AgentContract(ModelSchema):
    class Config:
        model = AgentEntity
        model_fields = "__all__"


class IdContract(Schema):
    id: int


class StudentInContract(AgentContract):
    user: UserSchema


class StudentOutContract(AgentContract, IdContract):
    user: UserSchema

    class Config:
        model = AgentEntity
        model_fields = ["user", "id"]


class StudentFlatContract(AgentContract, IdContract):
    class Config:
        model = AgentEntity
        model_fields = ["id"]


class ListContract(Schema):
    model: str
    count: int
    items: List[StudentFlatContract] = []


class FetchContract(Schema):
    model: str
    count: int
    item: StudentOutContract | None


class StudentListResponse(Schema):
    status: int
    data: ListContract


class StudentSingleResponse(Schema):
    status: int
    data: FetchContract
