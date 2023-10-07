from datetime import timedelta, datetime, UTC

import factory
from factory import fuzzy

from skii.platform.models.agent import TeacherAgent
from skii.platform.models.event import LessonEvent


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LessonEvent

    label = factory.Faker("text", max_nb_chars=80)
    description = factory.Faker("text", max_nb_chars=255)
    teacher = factory.Iterator(TeacherAgent.objects.all())
    start = fuzzy.FuzzyDateTime(
        start_dt=datetime.now(tz=UTC) - timedelta(hours=2),
        end_dt=datetime.now(tz=UTC),
        force_year=2023,
        force_month=7,
        # force_day=13,
    )
    stop = fuzzy.FuzzyDateTime(
        start_dt=datetime.now(tz=UTC),
        end_dt=datetime.now(tz=UTC) + timedelta(hours=4),
        force_year=2023,
        force_month=7,
        # force_day=13,
    )

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        """Permit to transmit students to link with lesson.

        Example:
         - event_objs = EventFactory.create(
               students=[
                   StudentAgentFactory(),
                   StudentAgentFactory()
               ]
           )
        """
        if not create or not extracted:
            return None
        self.students.add(*extracted)
