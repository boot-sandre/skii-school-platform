from typing import Literal

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Model
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from main.api import api as api_main
from skii.endpoint.api import api_skii


from skii.platform.entities import AgentEntity
from skii.platform.factories import (
    StudentAgentFactory,
    TeacherAgentFactory,
    LocationResourceFactory,
    LessonFactory,
    SuperUserFactory,
)


class SkiiTestClient(Client):
    """Custom api client dedicated to skii api."""

    def request(self, **request):
        """Always use application/json encoding"""
        request.setdefault("content_type", "application/json")
        return super().request(**request)

    def get(self, route_name, *args, **kwargs):
        url = reverse_lazy(route_name, args=args, kwargs=kwargs)
        return super().get(url, *args, **kwargs)

    def post(
        self,
        route_name,
        data=None,
        content_type="application/json",
        *args,
        headers=None,
        **extra,
    ):
        url = reverse_lazy(route_name)
        return super().post(
            url, data=data, content_type=content_type, *args, headers=headers, **extra
        )

    def delete(self, route_name, *args, **kwargs):
        url = reverse_lazy(route_name, args=args, kwargs=kwargs)
        return super().delete(url, *args, **kwargs)


class NinjaTestCase(TestCase):
    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        self.user = get_user_model().objects.create_user(
            username="user", email="simonandre@emencia.com", password="user"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="simon@emencia.com", password="admin"
        )
        self.user_client = self.client_class()
        self.user_client.force_login(self.user)
        self.admin_client = self.client_class()
        self.admin_client.force_login(self.admin_user)

    def link_api_helper(self):
        """Can override this method to link another project api to the test case."""
        self.api = api_main
        self.root_path = self.api.root_path
        self.docs_url = self.api.docs_url

    def setUp(self):
        self.create_client_helper()
        self.link_api_helper()


class SkiiClient(Client):
    pass


class SkiiTestCase(NinjaTestCase):
    client_class = SkiiClient
    api_factory = None
    api_save_contract = None
    api_route_namespace = None
    api_route_prefix = None

    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        res = super().create_client_helper()
        self.skii_client = self.client_class()
        self.skii_client.force_login(self.admin_user)
        return res

    def link_api_helper(self):
        """Override original method to link Skii API"""
        self.api = api_skii
        self.root_path = self.api.root_path
        self.docs_url = self.api.docs_url
        self.api_route_prefix = f"{self.root_path}{self.api_route_namespace}"


class SkiiControllerTestCase(TestCase):
    """ TestCase ninja api dedicated to skii platform.
    """
    # fixtures = ["profiles.yaml"]
    client_class = SkiiTestClient

    user_model: AbstractBaseUser = get_user_model()

    def client_auth(self, user: AbstractBaseUser) -> None:
        """Safest way to get a client with session registered.

        Args:
            user: Django user model instance
        """
        self.client.force_login(user)

    _superuser: AbstractBaseUser = None

    @property
    def superuser(self) -> AbstractBaseUser:
        """If superuser is None, create one use dedicated factory.

        In the other case return the superuser stored on self._superuser.
        """
        if self._superuser is not None:
            return self._superuser
        self._superuser = self.get_factory_instance("superuser")
        return self._superuser

    _client_superuser: SkiiTestClient = None

    @property
    def client_superuser(self) -> SkiiTestClient:
        """Return the skii superuser client logged with a superuser.

        If we already have a client, reuse it.
        Else need to ask django login.
        """
        if self._client_superuser is not None:
            return self._client_superuser
        self._client_superuser = self.client_class()
        self._client_superuser.force_login(self.superuser)
        return self._client_superuser

    @classmethod
    def _link_api(cls):
        """Override original method to link Skii API"""
        cls.api = api_skii
        cls.root_path = cls.api.root_path
        cls.docs_url = cls.api.docs_url

    @classmethod
    def setUpTestData(cls):
        cls._link_api()
        return super().setUpTestData()

    _factory_registry = {
        "student": StudentAgentFactory,
        "teacher": TeacherAgentFactory,
        "location": LocationResourceFactory,
        "lesson": LessonFactory,
        "superuser": SuperUserFactory,
    }

    def get_factory_instance(
        self,
        registry: Literal[
            "student", "teacher", "location", "lesson", "superuser"
        ] = "student",
        action: Literal["build", "create"] = "create",
    ) -> Model:
        """Helper to generate demodata with most used projects factories."""
        factory = self._factory_registry.get(registry)
        return getattr(factory, action)()
