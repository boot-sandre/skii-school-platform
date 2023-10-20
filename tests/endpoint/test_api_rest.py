# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from skii.platform.schemas.resource import LocationSaveContract
from ..testcase import SkiiTestCase
from skii.platform.schemas.agent import TeacherSaveContract, StudentSaveContract
from skii.platform.schemas.event import LessonSaveContract

from skii.platform.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
    LocationResourceFactory,
    LessonFactory,
)


class TestApiTeacher(SkiiTestCase):
    """Basic unit testing of Agent models and schema."""

    api_factory = TeacherAgentFactory
    api_save_contract = TeacherSaveContract
    api_route_namespace = "teacher"
    fields = ["user", "pk"]

    def test_record_fetch(self):
        record = self.api_factory.create()
        response = self.skii_client.get(
            path=f"{self.api_route_prefix}/fetch/{record.pk}/"
        )
        self.assertListEqual(list(response.json().keys()), self.fields)

    def test_record_list(self):
        self.api_factory.create_batch(5)
        response = self.skii_client.get(path=f"{self.api_route_prefix}/list/")
        self.assertEqual(first=response.status_code, second=200)
        self.assertEqual(first=len(response.json()), second=5)

    def test_record_delete(self):
        record = self.api_factory.create()
        response = self.skii_client.delete(
            path=f"{self.api_route_prefix}/delete/{record.pk}/"
        )
        assert response.content == b'{"message": "OK"}'

    def test_record_update(self):
        record = self.api_factory.create()
        payload = self.api_save_contract.from_orm(record).dict()
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/update/{record.pk}/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=self.fields)

    def test_record_create(self):
        record = self.api_factory.build()
        payload = self.api_save_contract.from_orm(record).dict()
        response = self.skii_client.post(
            path=f"{self.api_route_prefix}/create/",
            data=payload,
            content_type="application/json",
        )
        self.assertListEqual(list1=list(response.json().keys()), list2=self.fields)


class TestApiStudent(TestApiTeacher):
    """Basic unit testing of Agent models and schema."""

    api_factory = StudentAgentFactory
    api_save_contract = StudentSaveContract

    api_route_namespace = "student"
    fields = ["user", "pk"]


class TestApiLocation(TestApiTeacher):
    """Basic unit testing of Location models and schema."""

    api_factory = LocationResourceFactory
    api_save_contract = LocationSaveContract

    api_route_namespace = "location"
    fields = [
        "description",
        "label",
        "address1",
        "address2",
        "city",
        "country",
        "cover",
        "illustration",
        "coordinate",
        "value",
        "pk",
    ]


class TestApiLesson(TestApiTeacher):
    """Basic unit testing of Lesson models and schema."""

    api_factory = LessonFactory

    api_save_contract = LessonSaveContract

    api_route_namespace = "lesson"

    fixtures = ["profiles.yaml"]

    fields = [
        "pk",
        "gant_config",
        "start",
        "stop",
        "teacher",
        "students",
        "label",
        "description",
    ]
