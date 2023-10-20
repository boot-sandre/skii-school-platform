# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from datetime import datetime, timedelta, time, UTC, date
from typing import Dict, List, Literal, Any, Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Model
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from factory.django import DjangoModelFactory

from main.api import api as api_main
from skii.endpoint.api import api_skii
from skii.platform.entities import (
    AgentEntity,
    DatetimeRange,
    TimeRange,
    time_to_timedelta,
)

from skii.platform.factories import (
    StudentAgentFactory,
    TeacherAgentFactory,
    LocationResourceFactory,
    LessonFactory,
    SuperUserFactory,
)


import logging

from skii.platform.models.event import LessonEvent

logger = logging.getLogger(__name__)


class SkiiTestClient(Client):
    """Custom api client dedicated to skii api."""

    def request(self, **request):
        """Always use application/json encoding"""
        request.setdefault("content_type", "application/json")
        return super().request(**request)

    def get(self, route_name: str, data: Any = None, **extra: Any):
        """
        Perform a GET request to the API server.

        Args:
            route_name (str): The route name to use for resolving/reversing the URL.
                The format should be "api_name:route_name".
            data (Optional[dict]): A dictionary containing filter arguments
                if the API view implements Ninja Filters.
            **extra: Additional keyword arguments that will be used to resolve and
                integrate into the reversed URL.

        Returns:
            HttpResponse: The HTTP response from the GET request.

        Examples:
            >>> client = SkiiTestClient()
            >>> response = client.get("api:v1:event-detail", event_id=1)
            >>> response.status_code
            200

            Using Ninja Filters and event_id passed as kwargs:
            >>> client = SkiiTestClient()
            >>> filters = {"start_date": "2023-12-01", "end_date": "2023-12-15"}
            >>> response = client.get("api:v1:event-list", data=filters, event_id=1)
            >>> response.status_code
            200
        """
        url = reverse_lazy(route_name, kwargs=extra)
        return super().get(url, data=data, **extra)

    def post(
        self,
        route_name: str,
        data: Any = None,
        content_type: str = "application/json",
        *args: Any,
        headers: Optional[Dict[str, str]] = None,
        **extra: Any,
    ):
        """
        Perform a POST request to the API server.

        Args:
            route_name (str): The route name to use for resolving/reversing the URL.
                The format should be "api_name:route_name".
            data (Optional[dict]): Dictionary containing the data to
                include in the request body.
            content_type (str): Content type of the request
                (default is "application/json").
            *args: Additional positional arguments.
            headers (Optional[dict]): A dictionary containing custom HTTP headers
                to include in the request.
            **extra: Additional keyword arguments that will be used to resolve and
                integrate into the reversed URL.

        Returns:
            HttpResponse: The HTTP response from the POST request.

        Example:
            >>> client = SkiiTestClient()
            >>> data = {"name": "Ski Event", "location": "Ski Resort"}
            >>> response = client.post("api:v1:event-create", data=data)
            >>> response.status_code
            201
        """
        url = reverse_lazy(route_name, kwargs=extra)
        return super().post(
            url, data=data, content_type=content_type, *args, headers=headers, **extra
        )

    def delete(self, route_name, *args, **kwargs):
        url = reverse_lazy(route_name, args=args, kwargs=kwargs)
        return super().delete(url, *args, **kwargs)


class NinjaTestCase(TestCase):
    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        self.user = get_user_model().objects.create_user(
            username="user", email="simonandre@emencia.com", password="user"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", email="simon@emencia.com", password="admin"
        )
        self.user_client = self.client_class()
        self.user_client.force_login(self.user)
        self.admin_client = self.client_class()
        self.admin_client.force_login(self.admin_user)

    def link_api_helper(self):
        """Can override this method to link another project api to the test case."""
        self.api = api_main
        self.root_path = self.api.root_path
        self.docs_url = self.api.docs_url

    def setUp(self):
        self.create_client_helper()
        self.link_api_helper()


class SkiiClient(Client):
    pass


class SkiiTestCase(NinjaTestCase):
    client_class = SkiiClient
    api_factory = None
    api_save_contract = None
    api_route_namespace = None
    api_route_prefix = None

    def create_client_helper(self):
        """Create test user and log them to dedicated client."""
        res = super().create_client_helper()
        self.skii_client = self.client_class()
        self.skii_client.force_login(self.admin_user)
        return res

    def link_api_helper(self):
        """Override original method to link Skii API"""
        self.api = api_skii
        self.root_path = self.api.root_path
        self.docs_url = self.api.docs_url
        self.api_route_prefix = f"{self.root_path}{self.api_route_namespace}"


RegistryType: Literal = Literal["student", "teacher", "location", "lesson", "superuser"]


class SkiiDateLessonDemo:
    _skii_lesson_ranges: List[DatetimeRange] = []

    @classmethod
    def generate_skii_lesson_ranges(cls) -> None:
        """Generate a list of DatetimeRange objects

            The datetime object epresenting ski lesson dates for the month
            of December 2023.

        Returns:
            list: A list of DatetimeRange objects representing ski lesson dates.
        """
        # Early break if we already create the list of DatetimeRanges
        if cls._skii_lesson_ranges:
            return
        logger.info("Start DatetimeRange generation on project custom testcase")

        # Define the start/stop date of December 2023
        start_date = date(2023, 12, 1)
        stop_date = date(2023, 12, 31)

        # Stores opening hours for business days
        day_time_range = TimeRange(
            time(9, 00, 0, 0, UTC),  # 9:00 AM
            time(15, 00, 0, 0, UTC),  # 3:00 PM
        )

        # Time interval between ski lessons (e.g., 1 lesson every 2 hours)
        time_interval = timedelta(hours=2)
        offtime_interval = time_to_timedelta(day_time_range.stop, day_time_range.start)

        # Loops variable
        stop_datetime = datetime.combine(stop_date, day_time_range.stop, tzinfo=UTC)
        index_datetime = datetime.combine(start_date, day_time_range.start, tzinfo=UTC)
        # Loop to generate ski lesson dates for the entire month of December
        while index_datetime <= stop_datetime:
            # Create a DatetimeRange object for the current ski lesson
            lesson_start: datetime = index_datetime
            lesson_stop: datetime = index_datetime + time_interval
            lesson_datetime_range = DatetimeRange(start=lesson_start, stop=lesson_stop)
            lesson_time_range = TimeRange.from_datetime_range(lesson_datetime_range)

            # Check if the DatetimeRange is on the hours of lesson
            if lesson_time_range.is_contained_or_equal(day_time_range):
                logger.debug(f"{str(lesson_datetime_range)}")
                # Add the lesson start datetime to the list of ski lesson dates
                cls._skii_lesson_ranges.append(lesson_datetime_range)
            else:
                index_datetime += offtime_interval

            # Move to the next date by adding the time interval
            index_datetime += time_interval

    def test_generate_ski_lesson_dates(self) -> None:
        # Generate ski lesson dates
        self.generate_skii_lesson_ranges()

        # Verify that the list is not empty
        self.assertNotEqual(len(self._skii_lesson_ranges), 0)

        # Print the generated ski lesson dates
        for datetime_range in self._skii_lesson_ranges:
            logger.debug(str(datetime_range))


class SkiiLessonEventDemo:
    def _create_demo_lessons(self) -> None:
        """Create a sample of demo lessons."""
        teacher = self.get_factory_instance("teacher")
        teacher_other = self.get_factory_instance("teacher")
        self._teacher = teacher
        self._teacher_other = teacher_other
        student = self.get_factory_instance("student")
        student_other = self.get_factory_instance("student")
        self._student = student
        self._student_other = student_other

        lesson_teacher_payload = dict(teacher=teacher, students=[student])

        self.get_factory_instance("lesson", **lesson_teacher_payload)
        lesson_teacher_payload.update(students=[student, student_other])
        self.get_factory_instance("lesson", **lesson_teacher_payload)
        lesson_teacher_payload.update(students=[student_other])
        self.get_factory_instance("lesson", **lesson_teacher_payload)
        lesson_teacher_payload.update(students=[student_other], teacher=teacher_other)
        self.get_factory_instance("lesson", **lesson_teacher_payload)
        self.assertEqual(LessonEvent.objects.count(), 4)


class SkiiControllerTestCase(TestCase, SkiiDateLessonDemo, SkiiLessonEventDemo):
    """TestCase ninja api dedicated to skii platform."""

    client_class: Client = SkiiTestClient

    user_model: AbstractBaseUser = get_user_model()

    def client_auth(self, user: AbstractBaseUser | AgentEntity) -> None:
        """Safest way to authenticate the "self.client" with new session.

        Args:
            user: Django user model instance
        """
        if isinstance(user, AgentEntity):
            user = user.user
        self.client.force_login(user)
        logger.info(f"Testcase.client is authenticated as user {user}")

    _superuser: AbstractBaseUser = None

    @property
    def superuser(self) -> AbstractBaseUser:
        """If superuser is None, create one use dedicated factory.

        In the other case return the superuser stored on self._superuser.
        """
        if self._superuser is not None:
            return self._superuser
        self._superuser = self.get_factory_instance("superuser")
        logger.info(f"Testcase.superuser is created." f"(username: {self.superuser})")
        return self._superuser

    _client_superuser: SkiiTestClient = None

    @property
    def client_superuser(self) -> SkiiTestClient:
        """Return the skii superuser client logged with a superuser.

        If we already have a client, reuse it.
        Else need to ask django login.
        """
        if self._client_superuser is not None:
            return self._client_superuser
        self._client_superuser = self.client_class()
        self._client_superuser.force_login(self.superuser)
        logger.info(
            f"Testcase.client_superuser is authenticated as superuser "
            f"(username: {self.superuser})"
        )
        return self._client_superuser

    @classmethod
    def _link_api(cls) -> None:
        """Override original method to link Skii API"""
        cls.api = api_skii
        cls.root_path = cls.api.root_path
        cls.docs_url = cls.api.docs_url
        logger.info(f"Api {cls.api.title} is linked to testcase")

    @classmethod
    def setUpTestData(cls):
        """Link api to the testcase at class level.

        CAUTION: All unittest of a testcase will share same api instance.
                 If one unitest mutate the api instance,
                 it will be mutated for all next test
        """
        cls._link_api()
        cls.generate_skii_lesson_ranges()
        return super().setUpTestData()

    _factory_registry: Dict[str, RegistryType] = {
        "student": StudentAgentFactory,
        "teacher": TeacherAgentFactory,
        "location": LocationResourceFactory,
        "lesson": LessonFactory,
        "superuser": SuperUserFactory,
    }

    def get_factory(
        self,
        registry: RegistryType = "superuser",
    ) -> DjangoModelFactory:
        """Get most used projects factories stored on self._factory_registry."""
        logger.debug(f"Get factory from registry with key {registry}")
        return self._factory_registry.get(registry)

    def get_factory_instance(
        self,
        registry: RegistryType = "superuser",
        action: Literal["build", "create"] = "create",
        **kwargs,
    ) -> Model:
        """Get a builded or created demodata instance with most used factories."""
        factory: DjangoModelFactory = self._factory_registry.get(registry)
        logger.debug(
            f"Use factory from registry with key {registry} and action {action}",
            extra=kwargs,
        )
        return getattr(factory, action)(**kwargs)

    def assertDictKeys(self, dict_obj: Dict, keys: List[str], msg: str = None):
        """Check if dict keys are in a dict.

        Args:
            dict_obj: Asserted object
            keys: List of dict keys needs to be in dict_obj
            msg: Error message
        """
        self.assertIsInstance(dict_obj, dict, msg="First argument is not a dictionary")
        self.assertIsInstance(
            keys, list, msg="Second argument is not a list of keys or dict_keys"
        )
        dict_keys = dict_obj.keys()
        self.assertCountEqual(dict_keys, keys, "Needs have all dictionary keys")
        for key in keys:
            self.assertIn(key, dict_keys, msg=msg)
