from typing import List, Any

from django.db.models import Model
from ninja import Schema

from skii.endpoint.routers.abstract import RestRouterProducer
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.platform.models.resource import LocationResource
from skii.platform.schemas.common import CountryContract, GeoCoordinateContract


class AutomatedLocationRouter(RestRouterProducer):
    class Config(RestRouterProducer.Config):
        # Model Config
        model: Model = LocationResource
        name: str = "location"
        # Router config
        operation: List[str] = ["create", "read", "update", "delete", "list"]
        base_class: Schema = IntStrUUID4
        tags = ["lesson"]
        # Introspection config
        depth: int = 1
        save_depth: int = 0
        # Fields config/tweak
        fields: List[str] | None = None
        save_fields: List[str] | None = None
        exclude_fields: List[str] | None = ["uuid"]
        save_exclude_fields: List[str] | None = ["uuid"] + ["created", "last_modified"]
        custom_fields: List[tuple[Any, Any, Any]] | None = [
            (
                "country",
                CountryContract,
                CountryContract.parse_obj(dict(flag="", code="", name="")),
            ),
            (
                "coordinate",
                GeoCoordinateContract,
                GeoCoordinateContract.parse_obj(
                    dict(latitude=25.4536, longitude=70.4457)
                ),
            ),
        ]
        save_custom_fields: List[tuple[Any, Any, Any]] | None = None


LocationResourceRouter = AutomatedLocationRouter()

__all__ = [LocationResourceRouter]
