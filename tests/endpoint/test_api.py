from skii.platform.schemas.resource import LocationSaveContract
from ..testcase import SkiiTestCase
from skii.platform.schemas.agent import TeacherSaveContract, StudentSaveContract
from skii.platform.schemas.event import LessonSaveContract

from skii.platform.factories.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
    LocationResourceFactory,
    LessonFactory,
)


class TestApiTeacher(SkiiTestCase):
    """Basic unit testing of Agent models and schema."""

    api_factory = TeacherAgentFactory
    api_save_contract = TeacherSaveContract
    api_route_namespace = "teacher"
    fields = ["user", "pk"]

    def test_record_fetch(self):
        agent = self.api_factory.create()
        response = self.skii_client.get(
            path=f"{self.api_route_prefix}/fetch/{agent.pk}/"
        )
        self.assertListEqual(list(response.json().keys()), self.fields)

    def test_record_list(self):
        self.api_factory.create_batch(5)
        response = self.skii_client.get(path=f"{self.api_route_prefix}/list/")
        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(first=len(response.json()), second=5)

    def test_record_delete(self):
        agent = self.api_factory.create()
        response = self.skii_client.delete(
            path=f"{self.api_route_prefix}/delete/{agent.pk}/"
        )
        assert response.content == b'{"message": "OK"}'

    def test_record_update(self):
        agent = self.api_factory.create()
        payload = self.api_save_contract.from_orm(agent).dict()
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/update/{agent.pk}/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=self.fields)

    def test_record_create(self):
        agent = self.api_factory.build()
        payload = self.api_save_contract.from_orm(agent).dict()
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/create/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=self.fields)


class TestApiStudent(TestApiTeacher):
    """Basic unit testing of Agent models and schema."""

    api_factory = StudentAgentFactory
    api_save_contract = StudentSaveContract

    api_route_namespace = "student"
    fields = ["user", "pk"]


class TestApiLocation(TestApiTeacher):
    """Basic unit testing of Agent models and schema."""

    api_factory = LocationResourceFactory
    api_save_contract = LocationSaveContract

    api_route_namespace = "location"
    fields = ["country", "cover", "coordinate", "value"]


class TestApiLesson(TestApiTeacher):
    """Basic unit testing of Event models and schema."""

    api_factory = LessonFactory

    api_save_contract = LessonSaveContract

    api_route_namespace = "lesson"
    fields = []
