from typing import List, Type

from ninja import Schema
from django.db.models import Model


SkiiRecordContract: Schema = Type[Model]
SkiiListContract: Schema = List[Model]


class SkiiMsgContract(Schema):
    message: str


__all__ = [
    SkiiRecordContract,
    SkiiListContract,
    SkiiMsgContract,
]
