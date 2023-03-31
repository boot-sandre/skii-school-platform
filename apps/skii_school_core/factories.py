import factory
from django.conf import settings

from django.contrib.auth.hashers import make_password

from apps.skii_school_core.models import (
    StudentAgent,
    TeacherAgent,
    MoneyRessource,
    TimeRessource,
    Event,
    Location,
    GeoCoordinate,
    VisualAlbum,
    VisualElement,
    VisualPicture
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


latitude_config = {
    'left_digits': 3,
    'right_digits': 4,
    'positive': False,
    'min_value': -90,
    'max_value': 90,
}
longitude_config = latitude_config.copy()
longitude_config.update({
    'min_value': -180,
    'max_value': 180,
})


class GeoCoordinateFactory(factory.django.DjangoModelFactory):
    latitude = factory.Faker("pyfloat", **latitude_config)
    longitude = factory.Faker("pyfloat", **longitude_config)

    class Meta:
        model = GeoCoordinate


class VisualAlbumFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text")
    description = factory.Faker("text")

    class Meta:
        model = VisualAlbum


class VisualElementFactory(factory.django.DjangoModelFactory):
    album = factory.SubFactory(VisualAlbumFactory)

    title = factory.Faker("text")
    description = factory.Faker("text")
    picture = factory.django.ImageField()

    class Meta:
        model = VisualElement


class VisualPictureFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text")
    description = factory.Faker("text")
    picture = factory.django.ImageField()

    class Meta:
        model = VisualPicture


class LocationFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of an Event .
    """
    class Meta:
        model = Location
    address1 = factory.Faker("address")
    city = factory.Faker("city")
    country = factory.Faker("country_code")
    label = factory.Faker("text")
    description = factory.Faker("text")

    coordinate = factory.SubFactory(GeoCoordinateFactory)
    illustration = factory.SubFactory(VisualAlbumFactory)
    cover = factory.SubFactory(VisualPictureFactory)
