from typing import Optional

from ninja import Schema


class UserSchema(Schema):
    """Complete dj user schema generated from dj models

    Mostly to read records
    All technicals/Identifiant fields is excluded
    """
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    login: str


class UserSchemaShort(Schema):
    """Short dj user schema generated from dj models

    Mostly to create/edit/save record
    """
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    login: str


class StudentContract(Schema):
    user: UserSchema
    id: Optional[int]


class StudentContractShort(Schema):
    user: UserSchemaShort
    id: Optional[int]


class TeacherContract(Schema):
    user: UserSchema
    id: Optional[int]


class TeacherContractShort(Schema):
    user: UserSchemaShort
    id: Optional[int]
