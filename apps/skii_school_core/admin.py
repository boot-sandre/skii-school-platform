from django.contrib import admin
from .models import StudentAgent, TeacherAgent, GeoCoordinate
from .models import MoneyRessource, TimeRessource
from .models import Event, Location
from .models import VisualAlbum, VisualElement, VisualPicture
from .forms import EventForm, LocationForm


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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = [("title", "state"), ("start", "stop"), "teacher", "students"]
    form = EventForm
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
