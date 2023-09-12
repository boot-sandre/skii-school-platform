from typing import Optional

from ninja import Schema

from skii.skii_school_api.schemas import UserSchema, UserSchemaShort


class StudentContract(Schema):
    user: UserSchema
    id: [Optional]


class StudentContractShort(Schema):
    user: UserSchemaShort
    id: [Optional]


class TeacherContract(Schema):
    user: UserSchema
    id: [Optional]


class TeacherContractShort(Schema):
    user: UserSchemaShort
    id: [Optional]
