from datetime import datetime
from typing import Iterable

from django.db.models.query import QuerySet

from skii.platform.models.event import Lesson
from skii.platform.models.agent import StudentAgent, TeacherAgent


class AgendaInterface:
    @classmethod
    def list_student_lesson(
        cls,
        agent: TeacherAgent,
        date_range_start: datetime | None = None,
        date_range_stop: datetime | None = None,
    ) -> QuerySet[Lesson]:
        lesson_qs = Lesson.objects.all().filter(students=agent.id)
        if date_range_start is not None:
            lesson_qs = lesson_qs.filter(
                start__gt=date_range_start,
            )
        if date_range_stop is not None:
            lesson_qs = lesson_qs.filter(
                start__lt=date_range_stop,
            )
        return lesson_qs

    @classmethod
    def list_teacher_lesson(
        cls,
        agent: TeacherAgent,
        date_range_start: datetime | None = None,
        date_range_stop: datetime | None = None,
    ) -> QuerySet[Lesson]:
        lesson_qs = Lesson.objects.all().filter(teacher=agent.id)
        if date_range_start is not None:
            lesson_qs = lesson_qs.filter(
                start__gt=date_range_start,
            )
        if date_range_stop is not None:
            lesson_qs = lesson_qs.filter(
                start__lt=date_range_stop,
            )
        return lesson_qs

    @classmethod
    def create_lesson(
        cls,
        agent: TeacherAgent,
        date_range_start: datetime,
        date_range_stop: datetime,
        **kwargs,
    ) -> Lesson:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        payload.update(kwargs)
        lesson = Lesson.objects.create(**payload)
        return lesson

    @classmethod
    def get_or_create_lesson(
        cls,
        agent: TeacherAgent,
        date_range_start: datetime,
        date_range_stop: datetime,
        **defaults,
    ) -> Lesson:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        lesson = Lesson.objects.get_or_create(**payload, defaults=defaults)
        return lesson

    @classmethod
    def update_lesson(cls, lesson: Lesson, **values: dict) -> Lesson:
        for name, value in values.items():
            setattr(lesson, name, value)
        lesson.save()
        return lesson

    @classmethod
    def add_agents(cls, lesson: Lesson, students: Iterable[StudentAgent]) -> Lesson:
        lesson.students.add(*students)
        lesson.save()
        return lesson
