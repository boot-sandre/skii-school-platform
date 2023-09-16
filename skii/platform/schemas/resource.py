from ninja import Schema

from skii.platform.schemas.common import (
    CountryContract,
    VisualPictureContract,
    GeoCoordinateContract,
)


class LocationContract(Schema):
    country: CountryContract
    cover: VisualPictureContract | None
    coordinate: GeoCoordinateContract | None
    value: int = 1


class LocationSaveContract(LocationContract):
    country: str
