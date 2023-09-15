from ..testcase import SkiiTestCase
from skii.platform.schemas.agent import TeacherSaveContract, StudentSaveContract

from skii.platform.factories.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
)


class TestApiTeacher(SkiiTestCase):
    """Basic unit testing of Agent models and schema."""

    api_factory = TeacherAgentFactory
    api_save_contract = TeacherSaveContract
    api_route_namespace = "teacher"

    def test_agent_fetch(self):
        agent = self.api_factory.create()
        response = self.skii_client.get(
            path=f"{self.api_route_prefix}/fetch/{agent.pk}/"
        )
        self.assertListEqual(list(response.json().keys()), ["pk", "user"])

    def test_agent_list(self):
        self.api_factory.create_batch(5)
        response = self.skii_client.get(path=f"{self.api_route_prefix}/list/")
        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(first=len(response.json()), second=5)

    def test_agent_delete(self):
        agent = self.api_factory.create()
        response = self.skii_client.delete(
            path=f"{self.api_route_prefix}/delete/{agent.pk}/"
        )
        assert response.content == b'{"message": "OK"}'

    def test_agent_create(self):
        agent = self.api_factory.create()
        payload = TeacherSaveContract.from_orm(agent).dict()
        del payload["pk"]
        del payload["user"]["id"]
        payload["user"]["username"] = "unittest"
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/create/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=["pk", "user"])

    def test_agent_update(self):
        agent = self.api_factory.create()
        payload = self.api_save_contract.from_orm(agent).dict()
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/update/{agent.pk}/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=["pk", "user"])


class TestApiStudent(TestApiTeacher):
    """Basic unit testing of Agent models and schema."""

    api_factory = StudentAgentFactory
    api_save_contract = StudentSaveContract
    api_route_namespace = "student"
