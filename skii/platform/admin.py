from django.contrib import admin

from skii.platform.models.agent import (
    StudentAgent,
    TeacherAgent,
)
from skii.platform.models.common import (
    GeoCoordinate,
    VisualAlbum,
    VisualElement,
    VisualPicture,
)
from skii.platform.models.resource import (
    MoneyResource,
    TimeResource,
    LocationResource,
)
from skii.platform.models.event import (
    LessonEvent,
)

from .forms import LessonForm, LocationResourceForm


@admin.register(StudentAgent)
class StudentAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(TeacherAgent)
class TeacherAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(MoneyResource)
class MoneyResourceAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeResource)
class TimeResourceAdmin(admin.ModelAdmin):
    pass


@admin.register(LessonEvent)
class LessonAdmin(admin.ModelAdmin):
    fields = [("label", "state"), ("start", "stop"), "teacher", "students"]
    form = LessonForm
    date_hierarchy = "start"


@admin.register(LocationResource)
class LocationResourceAdmin(admin.ModelAdmin):
    fields = [
        "label",
        "description",
        ("address1", "address2"),
        ("city", "country"),
        "coordinate",
        ("cover", "illustration"),
    ]
    list_display = ["uuid", "label", "coordinate", "city", "country"]
    form = LocationResourceForm


@admin.register(GeoCoordinate)
class GeoCoordinateAdmin(admin.ModelAdmin):
    fields = [("latitude", "longitude")]


@admin.register(VisualAlbum)
class VisualAlbumAdmin(admin.ModelAdmin):
    fields = ["title", "description"]


@admin.register(VisualElement)
class VisualElementAdmin(admin.ModelAdmin):
    fields = ["album", "title", "description", "picture"]


@admin.register(VisualPicture)
class VisualPictureAdmin(admin.ModelAdmin):
    fields = ["title", "description", "picture"]
