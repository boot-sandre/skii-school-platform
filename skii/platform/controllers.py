from datetime import datetime
from typing import Iterable

from django.db.models.query import QuerySet

from skii.platform.models.event import LessonEvent
from skii.platform.models.agent import StudentAgent, TeacherAgent


class AgendaController:
    @classmethod
    def list_student_lesson(
        cls,
        agent: StudentAgent,
        date_range_start: datetime | None = None,
        date_range_stop: datetime | None = None,
    ) -> QuerySet[LessonEvent]:
        lesson_qs = LessonEvent.objects.all().filter(students__id=agent.id)
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
    ) -> QuerySet[LessonEvent]:
        lesson_qs = LessonEvent.objects.all().filter(teacher=agent)
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
    ) -> LessonEvent:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        payload.update(kwargs)
        lesson = LessonEvent.objects.create(**payload)
        return lesson

    @classmethod
    def get_or_create_lesson(
        cls,
        agent: TeacherAgent,
        date_range_start: datetime,
        date_range_stop: datetime,
        **defaults,
    ) -> LessonEvent:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        lesson = LessonEvent.objects.get_or_create(**payload, defaults=defaults)
        return lesson

    @classmethod
    def update_lesson(cls, lesson: LessonEvent, **values: dict) -> LessonEvent:
        for name, value in values.items():
            setattr(lesson, name, value)
        lesson.save()
        return lesson

    @classmethod
    def add_students(
        cls, lesson: LessonEvent, students: Iterable[StudentAgent]
    ) -> LessonEvent:
        lesson.students.add(*students)
        lesson.save()
        return lesson
