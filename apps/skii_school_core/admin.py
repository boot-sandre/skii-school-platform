from django.contrib import admin
from .models import StudentAgent, TeacherAgent
from .models import MoneyRessource, TimeRessource
from .models import Event, Location


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
    ordering = ["start", "stop", "state"]

    def save_model(self, request, obj, form, change):
        obj.user_creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
