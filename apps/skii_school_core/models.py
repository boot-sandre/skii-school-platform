import uuid

from django.utils.timezone import now
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from decimal import Decimal as D

from apps.account.forms.registration import User


class StudentAgent(models.Model):
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Student(s)"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    def __str__(self):
        return f"Student: {self.user.email}"


class TeacherAgent(models.Model):
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teacher(s)"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    def __str__(self):
        return f"Teacher: {self.user.email}"


class MoneyRessource(models.Model):
    class Meta:
        verbose_name = "Money"
        verbose_name_plural = "Money(s)"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    amount = MoneyField(
        "Money amount", max_digits=18, decimal_places=6,
        default=D(0.0), default_currency="EUR"
    )

    def __str__(self):
        return f"{str(self.uuid)[:6]}[...]: {self.amount}"


class TimeRessource(models.Model):
    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Time(s)"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    amount = models.FloatField("Time amount (seconds)", default=0.0)
    amount_planned = models.FloatField("Time planned (seconds)", default=600.0)

    def __str__(self):
        return f"{str(self.uuid)[:6]}[...]: {self.amount} sec / {self.amount_planned} sec"


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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    label = models.CharField(max_length=255, name="Label event")
    description = models.TextField()
    created = models.DateTimeField("Created", auto_now_add=True)
    last_modified = models.DateTimeField("Last Modified", auto_now=True)

    user_creator = models.ForeignKey(User, on_delete=models.PROTECT)

    state = models.CharField(max_length=128, choices=EVENTS_STATE, default="draft")

    start = models.DateTimeField("Start time", default=now)
    stop = models.DateTimeField("Stop time", default=now)
    agent_invited = models.ManyToManyField(User, blank=True, related_name="events")

    def __str__(self):
        return f"{str(self.label)}: {self.state} Date {self.start} / {self.stop} "


class Location(models.Model):
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Location(s)"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    label = models.CharField(max_length=255, default="New location")
    address1 = models.CharField(max_length=255, default="Address1")
    address2 = models.CharField(max_length=255, default="Address2",
                                blank=True, null=True)
    city = models.CharField(max_length=128, default="city")
    country = CountryField(multiple=False, default="EN")

    def __str__(self):
        return f"{self.label}: {self.city} / {self.country.name}"
