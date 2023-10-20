# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from .student import sub_route as route_student
from .teacher import sub_route as route_teacher
from .location import router as route_location
from .lesson import router as route_lesson
from .agenda import route_agenda

__all__ = [
    route_location,
    route_student,
    route_teacher,
    route_lesson,
    route_agenda,
]
