from skii.platform.models.event import LessonEvent
from tests.testcase import SkiiControllerTestCase

LESSON_KEYS = [
    "pk",
    "gant_config",
    "start",
    "stop",
    "teacher",
    "students",
    "label",
    "description",
]

USER_KEYS = [
    "pk",
    "first_name",
    "last_name",
    "username",
    "email",
]


class TestAgendaController(SkiiControllerTestCase):
    def setUp(self) -> None:
        res = super().setUp()
        self._create_teacher_lessons()
        return res

    _teacher = None
    _teacher_other = None

    def _create_teacher_lessons(self) -> None:
        """Create a sample of demo lessons."""
        teacher = self.get_factory_instance("teacher")
        teacher_other = self.get_factory_instance("teacher")
        self._teacher = teacher
        self._teacher_other = teacher_other
        lesson_teacher_payload = dict(teacher=teacher)

        self.get_factory_instance("lesson", **lesson_teacher_payload)
        self.get_factory_instance("lesson", **lesson_teacher_payload)
        self.get_factory_instance("lesson", **lesson_teacher_payload)

        self.get_factory_instance("lesson", **dict(teacher=teacher_other))
        self.assertEqual(LessonEvent.objects.count(), 4)

    def test_api_required_keys(self):
        """The response json have to contains dictionary keys of model serialized."""
        self.client_auth(self._teacher.user)
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher.pk
        )
        result = res.json()
        self.assertDictKeys(result, ["user", "pk", "lessons"])
        self.assertDictKeys(result["lessons"][0], LESSON_KEYS)
        self.assertDictKeys(result["user"], USER_KEYS)

    def test_count_teacher_lessons(self):
        """Fetch the 3 lessons related to self._teacher."""
        self.client_auth(self._teacher.user)
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher.pk
        )
        result = res.json()

        self.assertDictKeys(result, ["user", "pk", "lessons"])
        self.assertDictKeys(result["lessons"][0], LESSON_KEYS)
        self.assertDictKeys(result["user"], USER_KEYS)
        self.assertEqual(
            len(result["lessons"]),
            3,
            msg=f"Needs fetch only the 3 lessons related to teacher {self._teacher}",
        )

    def test_count_teacher_other_lessons(self):
        """Fetch the single lesson related to self._teacher_other."""
        self.client_auth(self._teacher_other.user)
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher_other.pk
        )
        result = res.json()

        self.assertEqual(
            len(result["lessons"]),
            1,
            msg=f"Needs fetch only the single lesson related "
            f"to other teacher {self._teacher_other}",
        )

    def test_cross_teacher_lesson(self):
        """Fetch teacher's lessons with other teacher account logged."""
        # We ask logging with self._teacher_other
        self.client_auth(self._teacher_other.user)
        # We fetch lessons of self._teacher
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher.pk
        )
        result = res.json()

        self.assertEqual(
            len(result["lessons"]),
            3,
            msg="Needs fetch the three lesson related of other "
            f"teacher {self._teacher_other}",
        )

    def test_teacher_lesson_range_start_to_stop(self):
        """Can fetch teacher lesson with range start/stop filter."""
        self.client_auth(self._teacher)
        lesson_ref: LessonEvent = LessonEvent.objects.filter(
            teacher=self._teacher
        ).first()
        res = self.client.get(
            "skii:teacher_lessons",
            dict(start=lesson_ref.start, stop=lesson_ref.stop),
            teacher_pk=str(self._teacher.pk),
        )
        result = res.json()
        self.assertEqual(
            len(result["lessons"]),
            3,
            msg=f"Needs fetch lesson after {lesson_ref.start}",
        )
