# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
import factory

from .common import GeoCoordinateFactory, VisualAlbumFactory, VisualPictureFactory
from skii.platform.models.resource import MoneyResource, TimeResource, LocationResource


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
