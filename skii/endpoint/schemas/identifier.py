from typing import Type

from ninja.schema import Schema
from pydantic import UUID4


IntStrUUID4: Type = UUID4 | int | str


class IntStrUUID4Contract(Schema):
    pk: IntStrUUID4


__all__ = [
    IntStrUUID4Contract,
    IntStrUUID4,
]
