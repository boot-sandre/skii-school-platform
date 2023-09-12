from typing import List, Any

from ninja import Schema


class NinjaResponse(Schema):
    data: Any | None


class NinjaListResponse(Schema):
    data: List[Any] = []
    model: str
    count: int
