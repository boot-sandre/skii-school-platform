from typing import List

from ninja import Router, NinjaAPI

from skii.endpoint.routers.mixins import (
    MixinsRestViewsProducer,
    MixinsRestSchemaProducer,
)
import logging


logger = logging.getLogger(__name__)


class RestRouterProducer(MixinsRestSchemaProducer, MixinsRestViewsProducer):
    """Generate standard Ninja REST router on a Dj model."""

    class Config(MixinsRestSchemaProducer.Config, MixinsRestViewsProducer.Config):
        tags: List[str] = []

    router: Router = None

    def __init__(self, *args, **kwargs):
        logger.info(f"Start to construct api router {self.Config.name} ")
        res = super().__init__(*args, **kwargs)
        self.mount()
        return res

    def mount(self):
        self.init_router()
        self.populate_view_operation()
        logger.info(f"Api routers {self.Config.name} is ready to mount now")

    def init_router(self):
        """Create Ninja Router instance."""
        logger.info(f"Initiate api routers {self.Config.name}")
        if self.router is None:
            self.router = Router(tags=self.Config.tags)

    def link_with_api(self, api: NinjaAPI):
        """Link router with an api provided."""
        logger.info(f"Mount router {self.Config.name} to API {api.title}")
        api.add_router(prefix=self.Config.name, router=self.router)
