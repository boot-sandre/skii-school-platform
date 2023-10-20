from skii.endpoint.routers.agenda import MsgErrorStudent
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
        self._create_demo_lessons()
        return res

    _teacher = None
    _teacher_other = None
    _student = None
    _student_other = None

    def test_teacher_lessons_required_keys(self):
        """The response json have to contains dictionary keys of model serialized."""
        self.client_auth(self._teacher.user)
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher.pk
        )
        result = res.json()
        self.assertDictKeys(result, ["user", "pk", "lessons_assigned"])
        self.assertDictKeys(result["lessons_assigned"][0], LESSON_KEYS)
        self.assertDictKeys(result["user"], USER_KEYS)

    def test_count_teacher_lessons(self):
        """Fetch the 3 lessons related to self._teacher."""
        self.client_auth(self._teacher.user)
        res = self.client.get(
            route_name="skii:teacher_lessons", teacher_pk=self._teacher.pk
        )
        result = res.json()

        self.assertEqual(
            len(result["lessons_assigned"]),
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
            len(result["lessons_assigned"]),
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
            len(result["lessons_assigned"]),
            3,
            msg="Needs fetch the three lesson related of other "
            f"teacher {self._teacher_other}",
        )

    def test_teacher_lesson_range_start_to_stop(self):
        """Can fetch teacher lesson with range start/stop filter."""
        self.client_auth(self._teacher)
        lesson_ref_start: LessonEvent = (
            LessonEvent.objects.filter(teacher=self._teacher).order_by("start").last()
        )
        lesson_ref_stop: LessonEvent = (
            LessonEvent.objects.filter(teacher=self._teacher).order_by("stop").last()
        )
        res = self.client.get(
            "skii:teacher_lessons",
            dict(start=lesson_ref_start.start, stop=lesson_ref_stop.stop),
            teacher_pk=str(self._teacher.pk),
        )
        result = res.json()
        self.assertEqual(
            len(result["lessons_assigned"]),
            1,
            msg=f"Needs fetch lesson start after {lesson_ref_start.start} "
            f"and stop before {lesson_ref_stop.stop}",
        )

    def test_student_lessons_required_keys(self):
        """The response json have to contains dictionary keys of model serialized."""
        self.client_auth(self._student.user)
        res = self.client.get(
            route_name="skii:student_lessons", student_pk=self._student.pk
        )
        result = res.json()
        self.assertDictKeys(result, ["user", "pk", "lessons_subscribed"])
        self.assertDictKeys(result["lessons_subscribed"][0], LESSON_KEYS)
        self.assertDictKeys(result["user"], USER_KEYS)

    def test_count_student_lessons(self):
        """Fetch the 2 lessons related to self._student."""
        self.client_auth(self._student.user)
        res = self.client.get(
            route_name="skii:student_lessons", student_pk=self._student.pk
        )
        result = res.json()

        self.assertEqual(
            len(result["lessons_subscribed"]),
            2,
            msg=f"Needs fetch only the 3 lessons related to student {self._student}",
        )

    def test_count_student_other_lessons(self):
        """Fetch the three lesson related to self._student_other."""
        self.client_auth(self._student_other.user)
        res = self.client.get(
            route_name="skii:student_lessons", student_pk=self._student_other.pk
        )
        result = res.json()

        self.assertEqual(
            len(result["lessons_subscribed"]),
            3,
            msg=f"Needs fetch only the single lesson related "
            f"to other student {self._student_other}",
        )

    def test_cross_student_lesson_forbidden(self):
        """Fetch student's lessons with other student account logged is forbidden."""
        # We ask logging with self._student_other
        self.client_auth(self._student_other.user)
        # We fetch lessons of self._student
        with self.assertRaises(PermissionError) as pm:
            self.client.get(
                route_name="skii:student_lessons", student_pk=self._student.pk
            )
        assert pm.exception
        self.assertEqual(pm.exception.__str__(), MsgErrorStudent)

    def test_teacher_can_fetch_student_lesson(self):
        """Fetch student's lessons with a teacher account logged is authorized."""
        self.client_auth(self._teacher.user)
        res = self.client.get(
            route_name="skii:student_lessons", student_pk=self._student.pk
        )
        assert res.status_code == 200

    def test_student_lesson_range_start_to_stop(self):
        """Can fetch student lesson with range start/stop filter."""
        self.client_auth(self._student)
        lesson_ref_start: LessonEvent = (
            LessonEvent.objects.filter(students=self._student).order_by("start").last()
        )
        lesson_ref_stop: LessonEvent = (
            LessonEvent.objects.filter(students=self._student).order_by("stop").last()
        )
        res = self.client.get(
            "skii:student_lessons",
            dict(start=lesson_ref_start.start, stop=lesson_ref_stop.stop),
            student_pk=str(self._student.pk),
        )
        result = res.json()
        self.assertEqual(
            len(result["lessons_subscribed"]),
            1,
            msg=f"Needs fetch lesson start after {lesson_ref_start.start} "
            f"and stop before {lesson_ref_stop.stop}",
        )

    def test_student_lesson_filter_only_start(self):
        """Can fetch student lesson with only start filter."""
        self.client_auth(self._student)
        lesson_ref: LessonEvent = (
            LessonEvent.objects.filter(students=self._student).order_by("start").last()
        )
        res = self.client.get(
            "skii:student_lessons",
            dict(start=lesson_ref.start),
            student_pk=str(self._student.pk),
        )
        result = res.json()
        self.assertEqual(
            len(result["lessons_subscribed"]),
            1,
            msg=f"Needs fetch lesson start after {lesson_ref.start}",
        )

    def test_student_lesson_filter_only_stop(self):
        """Can fetch student lesson with only stop filter."""
        self.client_auth(self._student)
        lesson_ref: LessonEvent = (
            LessonEvent.objects.filter(students=self._student).order_by("stop").first()
        )
        res = self.client.get(
            "skii:student_lessons",
            dict(stop=lesson_ref.stop),
            student_pk=str(self._student.pk),
        )
        result = res.json()
        self.assertEqual(
            len(result["lessons_subscribed"]),
            1,
            msg=f"Needs fetch lesson stop before {lesson_ref.stop}",
        )
