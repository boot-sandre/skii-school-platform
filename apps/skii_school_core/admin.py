from django.contrib import admin
from .models import StudentAgent, TeacherAgent
from .models import MoneyRessource, TimeRessource
from .models import Event, Location
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
    fields = [("label", "state"), ("start", "stop"), "agent_invited"]
    form = EventForm
    date_hierarchy = "start"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fields = ["label", "description", "country", ("address1", "address2"), "city"]
    form = LocationForm
