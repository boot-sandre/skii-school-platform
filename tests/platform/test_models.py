from skii.platform.schemas.resource import LocationContract
from ..testcase import SkiiTestCase

from skii.platform.factories.factories import (
    TeacherAgentFactory,
    StudentAgentFactory, LocationResourceFactory,
)


class TestAgent(SkiiTestCase):
    """Basic unit testing of Agent models and schema."""

    def test_agent_student_create(self):
        student = StudentAgentFactory.create()
        assert student.user
        serialized_user = student.user.__dict__
        assert serialized_user["username"]
        assert serialized_user["is_active"]

    def test_agent_teacher_create(self):
        teacher = TeacherAgentFactory.create()
        assert teacher.user
        serialized_user = teacher.user.__dict__
        assert serialized_user["username"]
        assert serialized_user["is_active"]

    def test_resource_location_create(self):
        location = LocationResourceFactory.create()
        location_payload = LocationContract.from_orm(location)
        self.assertEquals(location_payload.value, 1,
                          "Default resource value have to be one")
