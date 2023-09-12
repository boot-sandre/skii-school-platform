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
from skii.platform.models.ressource import (
    MoneyRessource,
    TimeRessource,
)
from skii.platform.models.event import (
    Lesson,
    Location,
)

from .forms import LessonForm, LocationForm


@admin.register(StudentAgent)
class StudentAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(TeacherAgent)
class TeacherAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(MoneyRessource)
class MoneyRessourceAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeRessource)
class TimeRessourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = [("label", "state"), ("start", "stop"), "teacher", "students"]
    form = LessonForm
    date_hierarchy = "start"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fields = [
        "label",
        "description",
        ("address1", "address2"),
        ("city", "country"),
        "coordinate",
        ("cover", "illustration"),
    ]
    list_display = ["uuid", "label", "coordinate", "city", "country"]
    form = LocationForm


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
