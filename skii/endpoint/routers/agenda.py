# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from ninja import Router, Query

from apps.base.schemas import FormInvalidResponseContract
from skii.endpoint.filters import LessonFilterSchema

from skii.platform.models.agent import TeacherAgent, StudentAgent
from skii.endpoint.schemas.response import TeacherLessonContract
from skii.endpoint.schemas.response import StudentLessonContract
from skii.endpoint.schemas.identifier import IntStrUUID4
from skii.platform.models.event import LessonEvent

UserModel = get_user_model()
MsgErrorStudent = _(
    "Fetch student lessons with another student account "
    "logged is forbidden. Please contact your support."
)

route_agenda = Router(tags=["skii", "agenda"])

RouterModel = LessonEvent


@route_agenda.get(
    path="/teacher_lessons/{teacher_pk}/",
    response={
        200: TeacherLessonContract,
        422: FormInvalidResponseContract,
    },
)
def teacher_lessons(
    request: HttpRequest,
    teacher_pk: IntStrUUID4,
    filters: LessonFilterSchema = Query(...),
):
    """Fetch teacher with them lessons assigned.

    This view permit's to use query filters:
        - start: Datetime to filter lesson start up to
        - stop: Datetime to filter lesson stop down to
    """
    agent = TeacherAgent.objects.get(pk=teacher_pk)
    lessons = filters.filter(LessonEvent.objects.filter(teacher__pk=agent.pk))
    setattr(agent, "lessons_assigned", lessons)
    return 200, agent


@route_agenda.get(
    path="/student_lessons/{student_pk}/",
    response={
        200: StudentLessonContract,
        422: FormInvalidResponseContract,
    },
)
def student_lessons(
    request: HttpRequest,
    student_pk: IntStrUUID4,
    filters: LessonFilterSchema = Query(...),
):
    """Fetch student with them lessons reserved.

    This view permit's to use query filters:
        - start: Datetime to filter lesson start up to
        - stop: Datetime to filter lesson stop down to

    They can be used independently, or together.

    Security:   Pending an implementation of more advanced rights,
                we will simply prohibit lesson requests from a student
                other than the connected user.
    """
    agent = StudentAgent.objects.get(pk=student_pk)
    # If the logged user is a Student (filter(user=request.user).exist())
    # and different than the requested one (request.user)
    # Raise a Permission error.
    if (
        request.user != agent.user
        and StudentAgent.objects.filter(user=request.user).exists()
    ):
        raise PermissionError(MsgErrorStudent)

    lessons = filters.filter(LessonEvent.objects.filter(students__pk=agent.pk))
    setattr(agent, "lessons_subscribed", lessons)

    return 200, agent
