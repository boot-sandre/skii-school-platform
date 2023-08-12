from django.contrib import admin

from .models import StudentAgent, TeacherAgent
from .models import CurrencyRessource, WorktimeRessource, Event


@admin.register(StudentAgent)
class StudentAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(TeacherAgent)
class TeacherAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrencyRessource)
class CurrencyRessourceAdmin(admin.ModelAdmin):
    pass


@admin.register(WorktimeRessource)
class WorktimeRessourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = [("name", "state"), ("start", "stop"), "agent_invited"]
    ordering = ["start", "stop", "state", "name"]

    def save_model(self, request, obj, form, change):
        obj.user_creator = request.user
        super().save_model(request, obj, form, change)
