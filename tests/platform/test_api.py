from ..testcase import NinjaTestCase


from skii.platform.factories.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
    TimeRessourceFactory,
    MoneyRessourceFactory,
    LessonFactory,
)


class TestSkiiPlatform(NinjaTestCase):
    def test_create_fixtures(self):
        teachers = TeacherAgentFactory.create_batch(5)
        assert len(teachers) == 5
        students = StudentAgentFactory.create_batch(15)
        assert len(students) == 15
        lessons = LessonFactory.create_batch(5)
        assert len(lessons) == 5
        moneys = MoneyRessourceFactory.create_batch(20)
        assert len(moneys) == 20
        times = TimeRessourceFactory.create_batch(20)
        assert len(times) == 20
