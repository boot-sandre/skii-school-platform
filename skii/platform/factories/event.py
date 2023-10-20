# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from datetime import timedelta, datetime, UTC

from django.db.models import Model
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
    )
    stop = fuzzy.FuzzyDateTime(
        start_dt=datetime.now(tz=UTC),
        end_dt=datetime.now(tz=UTC) + timedelta(hours=4),
        force_year=2023,
        force_month=7,
    )

    @factory.post_generation
    def students(self, create, extracted):
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

    @classmethod
    def _after_postgeneration(cls, instance: Model, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            instance.save()
