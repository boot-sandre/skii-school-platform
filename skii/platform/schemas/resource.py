# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import Optional

from ninja import ModelSchema, Field

from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.platform.models.resource import LocationResource
from skii.platform.schemas.common import (
    CountryContract,
    VisualPictureContract,
    GeoCoordinateContract,
    GeoCoordinateSaveContract,
    VisualAlbumContract,
)


class LocationContract(ModelSchema):
    class Config:
        model = LocationResource
        model_fields = [
            "description",
            "label",
            "address1",
            "address2",
            "city",
            "country",
            "cover",
            "illustration",
            "coordinate",
            "value",
        ]
        model_fields_optional = ["description", "address2"]

    pk: IntStrUUID4
    country: CountryContract
    cover: VisualPictureContract | None
    illustration: VisualAlbumContract | None
    coordinate: GeoCoordinateContract | None
    value: int = 1


class LocationSaveContract(ModelSchema):
    class Config:
        model = LocationResource
        model_fields = [
            "description",
            "label",
            "address1",
            "address2",
            "city",
            "coordinate",
            "value",
            "country",
        ]
        model_fields_optional = ["description", "address2"]

    coordinate: Optional[GeoCoordinateSaveContract]
    country: str = Field(default="", alias="country.code")
    # cover: VisualPictureContract | None
    value: int = 1
