# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from skii.platform.factories.agent import (
    SuperUserFactory,
    UserFactory,
    UserStaffFactory,
    StudentAgentFactory,
    TeacherAgentFactory,
)
from skii.platform.factories.resource import (
    MoneyResourceFactory,
    TimeResourceFactory,
    LocationResourceFactory,
)
from skii.platform.factories.event import LessonFactory
from skii.platform.factories.common import (
    GeoCoordinateFactory,
    VisualAlbumFactory,
    VisualPictureFactory,
    VisualElementFactory,
)

__all__ = [
    # auth.user
    UserFactory,
    UserStaffFactory,
    SuperUserFactory,
    # AgentEntity
    StudentAgentFactory,
    TeacherAgentFactory,
    # ResourceEntity
    MoneyResourceFactory,
    TimeResourceFactory,
    LocationResourceFactory,
    # Event Entity
    LessonFactory,
    # Common/Other models
    GeoCoordinateFactory,
    VisualAlbumFactory,
    VisualPictureFactory,
    VisualElementFactory,
]
