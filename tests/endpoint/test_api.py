from django.test.client import Client
from skii.endpoint.api import api_skii
from ..testcase import NinjaTestCase
from skii.platform.schemas.agent import TeacherSaveContract

from skii.platform.factories.factories import (
    TeacherAgentFactory,
)


class SkiiClient(Client):
    pass


class TestApiAgent(NinjaTestCase):
    """ Basic unit testing of Agent models and schema.
    """
    client_class = SkiiClient

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

    def test_agent_teacher_fetch(self):
        teacher = TeacherAgentFactory.create()
        response = self.skii_client.get(
            path=f"{self.teacher_url}/fetch/{teacher.pk}/")
        self.assertListEqual(
            list(response.json().keys()),
            ['pk', 'user'])

    def test_agent_teacher_list(self):
        TeacherAgentFactory.create_batch(5)
        response = self.skii_client.get(path=f"{self.teacher_url}/list/")
        self.assertEqual(first=response.status_code,
                         second=200)
        self.assertEqual(first=len(response.json()),
                         second=5)

    def test_agent_teacher_delete(self):
        teacher = TeacherAgentFactory.create()
        response = self.skii_client.delete(
            path=f"{self.teacher_url}/delete/{teacher.pk}/")
        assert response.content == b'{"message": "OK"}'

    def test_agent_teacher_create(self):
        teacher = TeacherAgentFactory.create()
        payload = TeacherSaveContract.from_orm(teacher).dict()
        del payload["pk"]
        del payload["user"]["id"]
        payload["user"]["username"] = "unittest"
        response = self.skii_client.post(
            path=f"{self.teacher_url}/create/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(
            list1=list(response.json().keys()),
            list2=['pk', 'user'])

    def test_agent_teacher_update(self):
        teacher = TeacherAgentFactory.create()
        payload = TeacherSaveContract.from_orm(teacher).dict()
        response = self.skii_client.post(
            path=f"{self.teacher_url}/update/{teacher.pk}/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(
            list1=list(response.json().keys()),
            list2=['pk', 'user'])
