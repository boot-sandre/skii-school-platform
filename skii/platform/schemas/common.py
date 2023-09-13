from decimal import Decimal
from datetime import datetime, timedelta
from typing import Optional
from ninja import Schema


class TimeRangeContract(Schema):
    start: datetime
    stop: datetime
    delta: Optional[timedelta]


class GeoCoordinateContract(Schema):
    latitude: Decimal
    longitude: Decimal


class CountryContract(Schema):
    code: str
    name: str
    flag: str


class VisualPictureContract(Schema):
    picture_url: str
    title: str
