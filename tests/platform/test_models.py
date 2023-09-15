from ..testcase import SkiiTestCase

from skii.platform.factories.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
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
