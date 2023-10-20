# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
import factory

from skii.platform.constants import LATITUDE_RANGE_CONFIG, LONGITUDE_RANGE_CONFIG
from skii.platform.models.common import (
    VisualElement,
    VisualAlbum,
    VisualPicture,
    GeoCoordinate,
)


class GeoCoordinateFactory(factory.django.DjangoModelFactory):
    latitude = factory.Faker("pydecimal", **LATITUDE_RANGE_CONFIG)
    longitude = factory.Faker("pydecimal", **LONGITUDE_RANGE_CONFIG)

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
