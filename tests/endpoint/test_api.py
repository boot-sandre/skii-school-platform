from ..testcase import SkiiTestCase, SkiiClient
from skii.platform.schemas.agent import TeacherSaveContract

from skii.platform.factories.factories import (
    TeacherAgentFactory,
)


class TestApiAgent(SkiiTestCase):
    """ Basic unit testing of Agent models and schema.
    """
    client_class = SkiiClient
    api_factory = TeacherAgentFactory
    api_save_contract = TeacherSaveContract

    def test_agent_teacher_fetch(self):
        teacher = TeacherAgentFactory.create()
        response = self.skii_client.get(
            path=f"{self.teacher_url}/fetch/{teacher.pk}/")
        self.assertListEqual(
            list(response.json().keys()),
            ['pk', 'user'])

    def test_agent_teacher_list(self):
        self.api_factory.create_batch(5)
        response = self.skii_client.get(path=f"{self.teacher_url}/list/")
        self.assertEqual(first=response.status_code,
                         second=200)
        self.assertEqual(first=len(response.json()),
                         second=5)

    def test_agent_teacher_delete(self):
        teacher = self.api_factory.create()
        response = self.skii_client.delete(
            path=f"{self.teacher_url}/delete/{teacher.pk}/")
        assert response.content == b'{"message": "OK"}'

    def test_agent_teacher_create(self):
        teacher = self.api_factory.create()
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
        teacher = self.api_factory.create()
        payload = self.api_save_contract.from_orm(teacher).dict()
        response = self.skii_client.post(
            path=f"{self.teacher_url}/update/{teacher.pk}/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(
            list1=list(response.json().keys()),
            list2=['pk', 'user'])
