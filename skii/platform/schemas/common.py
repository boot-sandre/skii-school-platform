# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
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
