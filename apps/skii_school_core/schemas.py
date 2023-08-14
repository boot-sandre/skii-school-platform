from ninja import Schema, ModelSchema
from apps.skii_school_core.entities import (
    StateEntity,
    AgentEntity,
)
from typing import Dict, List, Any, Union, Iterable


class StatusContract(Schema):
    status: int


class MessageResponseContract(StatusContract):
    message: str


class DataResponseContract(StatusContract):
    data: Union[Dict, List]


class FormErrorsResponseContract(StatusContract):
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
#


class StateContract(ModelSchema):
    class Config:
        model = StateEntity
        model_fields = ["state"]


class AgentContract(ModelSchema):
    class Config:
        model = AgentEntity
        model_fields = ["user"]


class IdContract(Schema):
    id: int


class StudentInContract(AgentContract):
    pass


class StudentOutContract(AgentContract, IdContract):
    pass


class ListContract(Schema):
    model: str
    count: int
    items: List[StudentOutContract] = []


class StudentListContract(StatusContract):
    data: ListContract


class GetContract(Schema):
    model: str
    count: int
    item: StudentOutContract | None


class StudentSingleContract(StatusContract):
    data: GetContract
