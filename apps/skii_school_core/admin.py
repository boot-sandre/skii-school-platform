from django.contrib import admin

from .models import CompanyAgent, StudentAgent, TeacherAgent
from .models import CurrencyRessource, WorktimeRessource, Event


@admin.register(CompanyAgent)
class CompanyAgentAdmin(admin.ModelAdmin):
    pass


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
    pass

