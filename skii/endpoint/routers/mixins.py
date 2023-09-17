import logging
from typing import List, Any

from django.db import models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Schema
from ninja.orm import create_schema

from skii.endpoint.schemas.ninja import FormInvalidResponseContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.endpoint.schemas.response import SkiiMsgContract

logger = logging.getLogger(__name__)


class MixinsRestViewsProducer:
    """Produce REST view and route.

    These routes will be registered on a Ninja api router.
    """

    class Config:
        operation: List[str] = ["create", "read", "update", "delete", "list"]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "router"):
            raise ValueError(
                "MixinsRestViewsProducer needs be mixed with "
                "skii.endpoint.schema.generator.RestRouterProducer"
            )
        super().__init__(*args, **kwargs)

    def populate_view_operation(self):
        """Add Create/Read/Update/Delete/List view to have a REST like API."""
        for op in self.Config.operation:
            add_view_func = getattr(self, f"add_view_{op}")
            add_view_func()

    def add_view_create(self):
        router = self.router
        router_model = self.Config.model
        save_contract = self.save_contract

        @router.post(
            path="/create/",
            response={
                200: self.contract,
                422: FormInvalidResponseContract,
            },
        )
        def record_create(request: HttpRequest, payload: save_contract):
            record_payload = payload.dict()
            record = router_model(**record_payload)
            record.save()
            record.refresh_from_db()
            return 200, record

    def add_view_read(self):
        router = self.router
        router_model = self.Config.model

        @router.get(
            path="/read/{pk}/",
            response={
                200: self.contract,
                422: FormInvalidResponseContract,
            },
        )
        def record_read(request: HttpRequest, pk: IntStrUUID4):
            return 200, get_object_or_404(router_model, pk=pk)

    def add_view_update(self):
        router = self.router
        router_model = self.Config.model
        save_contract = self.save_contract

        @router.post(
            path="/update/{pk}/",
            response={
                200: self.contract,
                422: FormInvalidResponseContract,
            },
        )
        def record_update(request: HttpRequest, pk: IntStrUUID4, payload: save_contract):
            record_payload = payload.dict()
            record = get_object_or_404(router_model, pk=pk)
            for attr, value in record_payload.items():
                setattr(record, attr, value)
            record.save()
            record.refresh_from_db()
            return 200, record

    def add_view_delete(self):
        router = self.router
        router_model = self.Config.model

        @router.get(
            path="/delete/{pk}/",
            response={
                200: SkiiMsgContract,
                422: FormInvalidResponseContract,
            },
        )
        def record_delete(request: HttpRequest, pk: IntStrUUID4):
            qs = router_model.objects.all().filter(pk=pk)
            if qs.exists():
                qs.delete()
            return 200, SkiiMsgContract(message="Record deleted")

    def add_view_list(self):
        router = self.router
        router_model = self.Config.model

        @router.get(
            path="/list/",
            response={
                200: self.list_contract,
                422: FormInvalidResponseContract,
            },
        )
        def record_list(request: HttpRequest):
            return 200, router_model.objects.all()


class MixinsRestSchemaProducer:
    contract: Schema = None
    save_contract: Schema = None
    list_contract: Any = None

    class Config:
        # Model Config
        model: models.Model | None = None
        name: str = "model"
        # Introspection config
        depth: int = 0
        save_depth: int = 0
        base_class: Schema = IntStrUUID4
        # Fields config/tweak
        fields: List[str] | None = None
        save_fields: List[str] | None = None
        exclude_fields: List[str] | None = None
        save_exclude_fields: List[str] | None = None
        custom_fields: List[tuple[Any, Any, Any]] | None = None
        save_custom_fields: List[tuple[Any, Any, Any]] | None = None

    def __init__(self, *args, **kwargs):
        """Autogenerate contract/schema from django models."""
        res = super().__init__(*args, **kwargs)
        self.contract = self.create_contract(
            fields=self.Config.fields,
            exclude_fields=self.Config.exclude_fields,
            custom_fields=self.Config.custom_fields,
            depth=self.Config.depth,
        )
        self.list_contract = List[self.contract]
        self.save_contract = self.create_contract(
            fields=self.Config.save_fields,
            exclude_fields=self.Config.save_exclude_fields,
            custom_fields=self.Config.save_custom_fields,
            depth=self.Config.save_depth,
        )
        return res

    def create_contract(
        self,
        fields: List[str] | None = None,
        exclude_fields: List[str] | None = None,
        custom_fields: List[tuple[Any, Any, Any]] | None = None,
        depth: int = 0,
    ):
        """Create read/response contract from dj models."""
        logger.debug(f"{self.Config.name} Contract custom fields {custom_fields}")
        logger.debug(f"{self.Config.name} Contract excluded fields {exclude_fields}")
        logger.debug(f"{self.Config.name} Contract included fields {fields}")
        logger.debug(f"{self.Config.name} inspection depth {depth}")

        contract = create_schema(
            model=self.Config.model,
            name=self.Config.name + "-contract",
            base_class=self.Config.base_class,
            depth=depth,
            exclude=exclude_fields,
            custom_fields=custom_fields,
            fields=fields,
        )

        contract_schema = contract.schema()

        logger.debug(
            f"{self.Config.name} Contract have fields {contract_schema['properties'].keys()}"
        )
        logger.debug(
            f"{self.Config.name} Contract have required fields  {contract_schema['required']}"
        )
        logger.debug(
            f"{self.Config.name} Save Contract have fields {contract_schema['properties'].keys()}"
        )
        logger.debug(
            f"{self.Config.name} Save Contract have required fields {contract_schema['required']}"
        )

        return contract
