from datetime import timedelta, datetime, UTC

import factory
from django.contrib.auth import get_user_model
from factory import fuzzy

from django.contrib.auth.hashers import make_password

from skii.platform.models.agent import (
    StudentAgent,
    TeacherAgent,
)
from skii.platform.models.common import (
    VisualElement,
    VisualAlbum,
    VisualPicture,
    GeoCoordinate,
)
from skii.platform.models.resource import (
    MoneyResource,
    TimeResource,
    LocationResource,
)
from skii.platform.models.event import (
    LessonEvent,
)


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create a fake standard dj user
    """

    class Meta:
        model = get_user_model()

    # Business fields
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = make_password("password")
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    # Technical fields
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


class UserStaffFactory(UserFactory):
    class Meta:
        model = get_user_model()

    is_staff: bool = True


class StudentAgentFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a student agent.
    """

    class Meta:
        model = StudentAgent

    user = factory.SubFactory(UserFactory)


class TeacherAgentFactory(factory.django.DjangoModelFactory):
    """Factory to create instance of a Teacher agent.

    Teacher agent have to be staff in order to access at the django
    administration and skii api docs.
    """

    class Meta:
        model = TeacherAgent

    user = factory.SubFactory(UserStaffFactory)


class MoneyResourceFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a Money resource.
    """

    class Meta:
        model = MoneyResource


class TimeResourceFactory(factory.django.DjangoModelFactory):
    """
    Factory to create instance of a time resource.
    """

    class Meta:
        model = TimeResource


latitude_config = {
    "left_digits": 3,
    "right_digits": 4,
    "positive": False,
    "min_value": -90,
    "max_value": 90,
}
longitude_config = latitude_config.copy()
longitude_config.update(
    {
        "min_value": -180,
        "max_value": 180,
    }
)


class GeoCoordinateFactory(factory.django.DjangoModelFactory):
    latitude = factory.Faker("pydecimal", **latitude_config)
    longitude = factory.Faker("pydecimal", **longitude_config)

    class Meta:
        model = GeoCoordinate


class VisualAlbumFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text", max_nb_chars=255)

    class Meta:
        model = VisualAlbum


class VisualElementFactory(factory.django.DjangoModelFactory):
    album = factory.SubFactory(VisualAlbumFactory)

    title = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text", max_nb_chars=255)
    picture = factory.django.ImageField()

    class Meta:
        model = VisualElement


class VisualPictureFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text", max_nb_chars=255)
    picture = factory.django.ImageField()

    class Meta:
        model = VisualPicture


class LocationResourceFactory(factory.django.DjangoModelFactory):
    """Factory to create instance of a geographic location/place."""

    class Meta:
        model = LocationResource

    address1 = factory.Faker("address")
    city = factory.Faker("city")
    country = factory.Faker("country_code")
    label = factory.Faker("text", max_nb_chars=80)
    description = factory.Faker("text", max_nb_chars=255)

    coordinate = factory.SubFactory(GeoCoordinateFactory)
    illustration = factory.SubFactory(VisualAlbumFactory)
    cover = factory.SubFactory(VisualPictureFactory)


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