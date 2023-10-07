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
