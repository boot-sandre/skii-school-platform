import factory

from skii.platform.constants import latitude_config, longitude_config
from skii.platform.models.common import (
    VisualElement,
    VisualAlbum,
    VisualPicture,
    GeoCoordinate,
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
