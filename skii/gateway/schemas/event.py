from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ninja import Schema

from skii.skii_school_api.schemas import (
    CountryContract,
    VisualPictureContract,
    GanttConfigContract,
    TeacherContract,
    StudentContract,
    GeoCoordinateContract,
)


class LessonContract(Schema):
    gant_config: GanttConfigContract
    start: datetime
    stop: datetime
    teacher: TeacherContract
    students: List[StudentContract] = []
    uuid: Optional[UUID] = uuid4


class LessonContractShort(LessonContract):
    pass


class LocationContract(Schema):
    country: CountryContract
    cover: VisualPictureContract | None
    coordinate: GeoCoordinateContract | None


class LocationContractShort(LocationContract):
    country: str

