import factory
from django.conf import settings

from django.contrib.auth.hashers import make_password

from apps.skii_school_core.models import (
    StudentAgent,
    TeacherAgent,
    MoneyRessource,
    TimeRessource,
    Event,
)


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create a fake user with Faker.
    """

    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = make_password("password")


class StudentAgentFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a student agent.
    """

    class Meta:
        model = StudentAgent

    user = factory.SubFactory(UserFactory)


class TeacherAgentFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Teacher agent.
    """

    class Meta:
        model = TeacherAgent

    user = factory.SubFactory(UserFactory)


class MoneyRessourceFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Money ressource.
    """

    class Meta:
        model = MoneyRessource


class TimeRessourceFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a time ressource.
    """

    class Meta:
        model = TimeRessource


class EventFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of an Event .
    """

    class Meta:
        model = Event

    editor = factory.SubFactory(UserFactory)
