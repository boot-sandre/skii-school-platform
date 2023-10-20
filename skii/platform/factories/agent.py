# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from skii.platform.models.agent import StudentAgent, TeacherAgent


class UserFactory(factory.django.DjangoModelFactory):
    """Create a fake standard dj user"""

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


class SuperUserFactory(UserStaffFactory):
    class Meta:
        model = get_user_model()

    username = "superuser"
    email = "contact@emencia.com"

    is_staff: bool = True
    is_superuser: bool = True


class StudentAgentFactory(factory.django.DjangoModelFactory):
    """Factory to create instance of a student agent."""

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
