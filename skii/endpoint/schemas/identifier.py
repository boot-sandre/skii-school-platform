from typing import Literal

from ninja.schema import Schema
from pydantic import UUID4, EmailStr


IntStrUUID4: Schema = Literal[int, str, UUID4]


__all__ = [
    IntStrUUID4,
    EmailStr,
    UUID4,
]
