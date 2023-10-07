from datetime import datetime, timedelta
from typing import Optional, List
from ninja import Schema, ModelSchema

from skii.platform.models.common import GeoCoordinate


class TimeRangeContract(Schema):
    start: datetime
    stop: datetime
    delta: Optional[timedelta]


class GeoCoordinateContract(ModelSchema):
    class Config:
        model = GeoCoordinate
        model_fields = ["latitude", "longitude"]


class GeoCoordinateSaveContract(ModelSchema):
    class Config:
        model = GeoCoordinate
        model_fields = ["latitude", "longitude"]


class CountryContract(Schema):
    code: str
    name: str
    flag: str


class CountrySaveContract(Schema):
    code: str


class VisualPictureContract(Schema):
    picture_url: str
    title: str
    description: str


class VisualElementContract(Schema):
    title: str
    description: str
    picture_url: str


class VisualAlbumContract(Schema):
    title: str
    description: str
    items: List[VisualElementContract]
