from typing import List, Any

from ninja import Schema
from pydantic import conint


class NinjaResponse(Schema):
    data: Any | None


class NinjaListResponse(Schema):
    data: List[Any] = []
    count: conint(gt=0)
