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
    lessons = LessonEvent.objects.all()
    lessons = filters.filter(lessons)
    agent = TeacherAgent.objects.get(pk=teacher_pk)
    setattr(agent, "lessons", lessons)
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
    if (request.user != agent.user and
            StudentAgent.objects.filter(user=request.user).exists()):
        raise PermissionError(MsgErrorStudent)
    lessons = LessonEvent.objects.all()
    lessons = filters.filter(lessons)
    # TODO: Here we have an issue to correctly filter agent.lessons
    #       Unittest test_student_lesson_filter_only_stop fail because of
    #       agent.lessons get all related agent's lesson
    setattr(agent, "lessons", lessons)
    return 200, agent
