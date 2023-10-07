from skii.platform.factories.agent import (
    UserFactory, UserStaffFactory, StudentAgentFactory, TeacherAgentFactory,
)
from skii.platform.factories.resource import (
    MoneyResourceFactory, TimeResourceFactory, LocationResourceFactory,
)
from skii.platform.factories.event import LessonFactory
from skii.platform.factories.common import (
    GeoCoordinateFactory, VisualAlbumFactory, VisualPictureFactory, VisualElementFactory
)

__all__ = [
    # auth.user
    UserFactory,
    UserStaffFactory,
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
    VisualElementFactory
]
