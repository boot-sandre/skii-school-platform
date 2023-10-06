from typing import Literal, Dict, List, Iterable

from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from main.api import api as api_main
from skii.endpoint.api import api_skii

from django.test import Client
from django.urls import reverse, reverse_lazy

from skii.platform.entities import AgentEntity
from skii.platform.models.agent import StudentAgent, TeacherAgent


class SkiiTestClient(Client):
    """ Custom api client dedicated to skii api."""
    def request(self, **request):
        """ Always use application/json encoding"""
        request.setdefault('content_type', 'application/json')
        return super().request(**request)

    def get(self, route_name, *args, **kwargs):
        url = reverse_lazy(route_name, args=args, kwargs=kwargs)
        return super().get(url, *args, **kwargs)

    def post(
            self,
            route_name,
            data=None,
            content_type='application/json',
            *args,
            headers=None,
            **extra):
        url = reverse_lazy(route_name)
        return super().post(url, data=data, content_type=content_type, *args, headers=headers, **extra)

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


class SkiiServiceTestCase(TestCase):
    fixtures = ["profiles.yaml"]
    client_class = SkiiTestClient

    User = get_user_model()

    def api_auth_user(self, user: User) -> None:
        """ .

        Safest way to get a client with credentials.

        Args:
            user: Django user model instance
        """
        self.client.force_login(user)

    _client_admin: SkiiTestClient = None

    @property
    def client_superuser(self):
        """ Return the skii superuser client logged."""
        if self._client_admin is not None:
            return self._client_admin
        self._client_admin = self.client_class()
        self._client_admin.force_login(
            get_user_model().objects.get(username="superuser"))
        return self._client_admin

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

    def setUp(self) -> None:
        super().setUp()
        self.profile_to_model["student"] = StudentAgent.objects.all()
        self.profile_to_model["teacher"] = TeacherAgent.objects.all()

    profile_to_model: Dict[str, Iterable[AgentEntity]] = {
        "student": [],
        "teacher": [],
    }

    def get_agent_registry(
            self, profile: Literal["student", "teacher"] = "student"):
        """ Helper to fetch teacher/student profile."""
        yield from self.profile_to_model[profile]

