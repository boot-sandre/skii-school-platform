import uuid
from decimal import Decimal as Deci
from django.utils.timezone import now

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class RecordIdentityHistory(models.Model):
    """To track and store on an object creation/update datetime."""

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name=_("Last Modified"), auto_now=True)


class UUIDEntity(RecordIdentityHistory):
    class Meta:
        abstract = True

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def short_prefix_uuid(self):
        return f"{str(self.uuid)[:8]}..."


class DisplayEntity(models.Model):
    class Meta:
        abstract = True

    label = models.CharField(max_length=255, verbose_name=_("Label/Title"))
    description = models.TextField(
        verbose_name=_("A long description to display"), blank=True, null=True
    )


class DescriptionEntity(models.Model):
    class Meta:
        abstract = True

    description_short = models.TextField(
        max_length=255, verbose_name=_("Short description"), blank=True, null=True
    )


class StateChoices(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PLANNED = "planned", _("Planned")
    IN_PROGRESS = "in_progress", _("In progress")
    CANCELLED = "cancelled", _("Cancelled")
    FINISHED = "finished", _("Finished")


def mutate_event_state(value, initial):
    print("mutate_event_state:value")
    print(value)
    print("mutate_event_state:initial")
    print(initial)

    new_status = initial
    if value == StateChoices.DRAFT and initial in [
        StateChoices.PLANNED,
        StateChoices.DRAFT,
        None,
    ]:
        new_status = value
    elif value == StateChoices.PLANNED and initial in [
        StateChoices.PLANNED,
        StateChoices.DRAFT,
    ]:
        new_status = value
    elif value == StateChoices.IN_PROGRESS and initial in [
        StateChoices.IN_PROGRESS,
        StateChoices.PLANNED,
    ]:
        new_status = value
    elif value == StateChoices.FINISHED and initial in [
        StateChoices.FINISHED,
        StateChoices.IN_PROGRESS,
    ]:
        new_status = value
    elif value == StateChoices.CANCELLED and initial in [
        StateChoices.CANCELLED,
        StateChoices.IN_PROGRESS,
        StateChoices.DRAFT,
        StateChoices.PLANNED,
    ]:
        new_status = value
    return new_status


class StateEntity(models.Model):
    class Meta:
        abstract = True

    state = models.CharField(
        max_length=32, choices=StateChoices.choices, default=StateChoices.DRAFT
    )

    def __str__(self):
        return str(self.state)


class AgendaEntity(UUIDEntity, DisplayEntity):
    class Meta:
        abstract = True

    start = models.DateTimeField(verbose_name=_("Start time"), default=now)
    stop = models.DateTimeField(verbose_name=_("Stop time"), default=now)


class AgentEntity(RecordIdentityHistory):
    class Meta:
        abstract = True
        verbose_name = _("Agent")
        verbose_name_plural = _("Agent(s)")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self._meta.model_name}: {self.user.get_username()}"


class RessourceEntity(UUIDEntity, DescriptionEntity):
    class Meta:
        abstract = True

    amount = models.DecimalField(
        verbose_name=_("Time ressource (seconds)"), default=Deci(0.0)
    )

    def __str__(self):
        return f"{self.short_prefix_uuid}: {self.amount}"
