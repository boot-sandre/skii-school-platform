from django.utils.timezone import now
from django.db import models
from decimal import Decimal as D

from django.db.models.signals import pre_save
from apps.account.forms.registration import User


class StudentAgent(models.Model):
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    def __str__(self):
        return f"Student: {self.user.email}"


class TeacherAgent(models.Model):
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    def __str__(self):
        return f"Teacher: {self.user.email}"


class CompanyAgent(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)


class CurrencyRessource(models.Model):
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currency(s)"

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)
    factor = models.DecimalField(
        "Price factor against dollars", max_digits=5, decimal_places=3, default=D(1.000)
    )
    quantity = models.DecimalField(
        "Price factor against dollars", max_digits=12, decimal_places=2, default=D(0.0)
    )

    def __str__(self):
        return f"{self.code}: {self.quantity} * {self.factor} = {self.quantity * self.factor}"


class WorktimeRessource(models.Model):
    class Meta:
        verbose_name = "Worktime"
        verbose_name_plural = "Worktime(s)"

    name = models.CharField(max_length=255, default="New work time ressource")
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)
    time_elasped = models.FloatField("Work time (seconds)", default=0.0)
    time_planned = models.FloatField("Time planned (seconds)", default=600.0)

    def __str__(self):
        return f"{self.name}: {self.time_elasped} / {self.time_planned}"


EVENTS_STATE = (
    ("draft", "Draft"),
    ("planned", "Planned"),
    ("in_progress", "In progress"),
    ("cancelled", "Cancelled"),
    ("postponed", "Postponed in time"),
    ("finished", "finished"),
)


class Event(models.Model):
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Event(s)"

    name = models.CharField(max_length=255, default="New events")
    state = models.CharField(max_length=128, choices=EVENTS_STATE, default="draft")
    user_creator = models.ForeignKey(User, on_delete=models.PROTECT)
    start = models.DateTimeField("Start time", default=now)
    stop = models.DateTimeField("Stop time", default=now)
    agent_invited = models.ManyToManyField(User, blank=True, related_name="events")

    def __str__(self):
        return f"{self.name}: {self.state} Date {self.start} / {self.stop}"


class Location(models.Model):
    name = models.CharField(max_length=255, default="New events")
