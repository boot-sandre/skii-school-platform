from datetime import datetime
from typing import Iterable

from django.db.models.query import QuerySet

from apps.skii_school_core.models import Event, StudentAgent, TeacherAgent


class AgendaInterface:
    @classmethod
    def list_student_event(cls,
                           agent: TeacherAgent,
                           date_range_start: datetime | None = None,
                           date_range_stop: datetime | None = None
                           ) -> QuerySet[Event]:
        event_qs = Event.objects.all().filter(
            students=agent.id
        )
        if date_range_start is not None:
            event_qs = event_qs.filter(
                start__gt=date_range_start,
            )
        if date_range_stop is not None:
            event_qs = event_qs.filter(
                start__lt=date_range_stop,
            )
        return event_qs

    @classmethod
    def list_teacher_event(cls,
                           agent: TeacherAgent,
                           date_range_start: datetime | None = None,
                           date_range_stop: datetime | None = None) -> QuerySet[Event]:
        event_qs = Event.objects.all().filter(
            teacher=agent.id
        )
        if date_range_start is not None:
            event_qs = event_qs.filter(
                start__gt=date_range_start,
            )
        if date_range_stop is not None:
            event_qs = event_qs.filter(
                start__lt=date_range_stop,
            )
        return event_qs

    @classmethod
    def create_event(cls,
                     agent: TeacherAgent,
                     date_range_start: datetime, date_range_stop: datetime,
                     **kwargs
                     ) -> Event:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        payload.update(kwargs)
        event = Event.objects.create(
            **payload
        )
        return event

    @classmethod
    def get_or_create_event(cls,
                            agent: TeacherAgent,
                            date_range_start: datetime, date_range_stop: datetime,
                            **defaults
                            ) -> Event:
        payload = {
            "start": date_range_start,
            "stop": date_range_stop,
            "teacher": agent,
        }
        event = Event.objects.get_or_create(
            **payload,
            defaults=defaults
        )
        return event

    @classmethod
    def update_event(cls,
                     event: Event,
                     **values: dict
                     ) -> Event:
        for name, value in values.items():
            setattr(event, name, value)
        event.save()
        return event

    @classmethod
    def add_agents(cls,
                   event: Event,
                   students: Iterable[StudentAgent]) -> Event:
        event.students.add(*students)
        event.save()
        return event
