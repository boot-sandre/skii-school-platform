from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from main.api import api as api_main
from skii.endpoint.api import api_skii


class NinjaTestCase(TestCase):
    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        self.user = get_user_model().objects.create_user(
            username="user", password="user"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin"
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

    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        res = super().create_client_helper()
        self.skii_client = self.client_class()
        self.skii_client.force_login(self.admin_user)
        return res

    def link_api_helper(self):
        """ Override original method to link Skii API"""
        self.api = api_skii
        self.root_path = self.api.root_path
        self.docs_url = self.api.docs_url
        self.student_route = "student"
        self.teacher_route = "teacher"
        self.student_url = f"{self.root_path}{self.student_route}"
        self.teacher_url = f"{self.root_path}{self.teacher_route}"


