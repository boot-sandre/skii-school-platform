# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from skii.platform.schemas.resource import LocationContract
from ..testcase import SkiiTestCase

from skii.platform.factories import (
    TeacherAgentFactory,
    StudentAgentFactory,
    LocationResourceFactory,
)


class TestAgent(SkiiTestCase):
    """Basic unit testing of Agent models and schema."""

    def test_agent_student_create(self):
        student = StudentAgentFactory.create()
        assert student.user
        serialized_user = student.user.__dict__
        assert serialized_user["username"]
        assert serialized_user["is_active"]

    def test_agent_teacher_create(self):
        teacher = TeacherAgentFactory.create()
        assert teacher.user
        serialized_user = teacher.user.__dict__
        assert serialized_user["username"]
        assert serialized_user["is_active"]

    def test_resource_location_create(self):
        location = LocationResourceFactory.create()
        location_payload = LocationContract.from_orm(location)
        self.assertEqual(
            location_payload.value, 1, "Default resource value have to be one"
        )
