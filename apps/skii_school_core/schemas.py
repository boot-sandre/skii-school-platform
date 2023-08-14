from ninja import Schema, ModelSchema
from apps.skii_school_core.entities import (
    DisplayEntity,
    DescriptionEntity,
    StateEntity,
    AgentEntity,
)
from typing import Dict, List, Any, Union


class ResponseContract(Schema):
    status: int


class MessageResponseContract(ResponseContract):
    message: str


class DataResponseContract(ResponseContract):
    data: Union[Dict, List]


class FormErrorsResponseContract(ResponseContract):
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

    # user__first_name: str
    # user__last_name: str
    # label: str
    # description: str | None
    # state: Literal[StateChoices.choices] = []
    # user: Any


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


class StudentListContract(ResponseContract):
    data: ListContract


class GetContract(Schema):
    model: str
    count: int
    item: StudentOutContract | None


class StudentGetContract(ResponseContract):
    data: GetContract
