import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal as Deci
from typing import Iterator

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django.db import models


class RecordIdentityHistory(models.Model):
    """Abstract model to track and store on an object

    creation/update datetime.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name=_("Last Modified"), auto_now=True)


class UUIDEntity(RecordIdentityHistory):
    """Abstract model to use uuid as primary key.

    UUID can give more flexibility with SaaS deployment, distribued data/db.
    Have impact compare to a typical integer id on database storage and performance.

    17/09/23
    --------
     * The best way to manage object identifier looks to use natural FK.
    """

    class Meta:
        abstract = True

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def short_prefix_guid(self):
        """Usefull for have short uuid preview."""
        return f"{str(self.guid)[:8]}..."


class DescribeEntity(models.Model):
    """Abstract model to add short description fields

    Give the capacity to a models to store a short record description about it.
    """

    class Meta:
        abstract = True

    description = models.TextField(
        max_length=255, verbose_name=_("Short description"), blank=True, null=True
    )


class DescribeFullEntity(models.Model):
    """Abstract model to add short and long description fields

    Give the capacity to store a long record description
    and a short one.

    TODO: May use ckeditor HTMLField with wysiwyg.
    """

    class Meta:
        abstract = True

    description = models.TextField(
        max_length=1020, verbose_name=_("Long description"), blank=True, null=True
    )
    description_short = models.TextField(
        max_length=255, verbose_name=_("Long description"), blank=True, null=True
    )


class LabelEntity(models.Model):
    """Abstract model to add a Label on a record

    Vue.js use mostly label property to display content.
    It's more usefully to keep same name back and front.

    Label field can be more universal than "title" semantic
    """

    class Meta:
        abstract = True

    label = models.CharField(max_length=80, verbose_name=_("Label"), default="")


class TitleEntity(models.Model):
    """Add a title on a record:

    Usefull for named content, like cms page, book, documents
    """

    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name=_("Title"), default="")


class ContentEntity(models.Model):
    """Main text content."""

    class Meta:
        abstract = True

    content = models.TextField(
        verbose_name=_("Full content to display"), blank=True, null=True
    )


class CMSDisplayEntity(TitleEntity, DescribeEntity):
    """Abstract model to cms element.

    Can be page, illustration, Document
    """

    class Meta:
        abstract = True


class NomenclatureEntity(LabelEntity, DescribeEntity):
    """To reference tags or other."""

    class Meta:
        abstract = True


class UUIDLabelEntity(UUIDEntity, NomenclatureEntity):
    class Meta:
        abstract = True


class CMSUUIDEntity(UUIDEntity, CMSDisplayEntity):
    class Meta:
        abstract = True

    def __str__(self):
        return f"[{self.pk}] {self.title[:30]}"


def get_default_cover_image():
    return "default.png"


class VisualEntity(CMSUUIDEntity):
    class Meta:
        abstract = True

    picture = models.ImageField(
        verbose_name=_("Picture"), default=get_default_cover_image
    )


class GeoCoordinateEntity(models.Model):
    class Meta:
        abstract = True
        index_together = [
            ["latitude", "longitude"],
        ]

    latitude = models.DecimalField(
        validators=[
            MaxValueValidator(limit_value=90),
            MinValueValidator(limit_value=-90),
        ],
        max_digits=6,
        decimal_places=4,
    )
    longitude = models.DecimalField(
        validators=[
            MaxValueValidator(limit_value=180),
            MinValueValidator(limit_value=-180),
        ],
        max_digits=7,
        decimal_places=4,
    )


class StateChoices(models.TextChoices):
    DRAFT = "draft", _("Draft")
    PLANNED = "planned", _("Planned")
    IN_PROGRESS = "in_progress", _("In progress")
    CANCELLED = "cancelled", _("Cancelled")
    FINISHED = "finished", _("Finished")


def mutate_event_state(value, initial):
    """Centralize state workflow condition."""
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
    """State usefully to establish record workflow condition.

    TODO: Use django signal with mutate_event_state
    """

    class Meta:
        abstract = True

    state = models.CharField(
        max_length=32, choices=StateChoices.choices, default=StateChoices.DRAFT
    )


@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError("Can not end before starting.")

    def __str__(self) -> str:
        return f"DateRange({self.start} - {self.end})"

    def __add__(self, other: timedelta) -> "DateRange":
        if isinstance(other, timedelta):
            return DateRange(self.start + other, self.end + other)

        raise TypeError()

    def hour_later(self) -> "DateRange":
        return self + timedelta(hours=1)

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def overlaps(self, date_range: "DateRange") -> bool:
        return (self.start <= date_range.end
            and self.end >= date_range.start)

    def starts_before(self, date_range: "DateRange") -> bool:
        return self.start < date_range.start

    def range(self, step: timedelta) -> Iterator[datetime]:
        current_datetime = self.start
        while current_datetime <= self.end:
            yield current_datetime
            current_datetime = current_datetime + step


class TimeRangeQueryset(models.QuerySet):

    def filter(self, *args, **kwargs):
        date_range = kwargs.get("date_range")

        if date_range and isinstance(date_range, DateRange):
            kwargs["start"] = date_range.start
            kwargs["end"] = date_range.end

        return super().filter(*args, **kwargs)


class TimeRangeManager(models.Manager):
    def get_queryset(self):
        return TimeRangeQueryset(self.model, using=self._db)

    def in_range(self, date_range: DateRange):
        return self.get_queryset().filter(
            start__gt=date_range.start,
            end__lt=date_range.end
         )


class TimeRangeEntity(models.Model):
    class Meta:
        abstract = True

    start = models.DateTimeField(verbose_name=_("Start time"), default=now)
    stop = models.DateTimeField(verbose_name=_("Stop time"), default=now)

    objects = TimeRangeManager()

    @property
    def date_range(self) -> DateRange:
        return DateRange(self.start, self.stop)

    @date_range.setter
    def date_range(self, value: DateRange) -> None:
        self.start = value.start
        self.stop = value.end

    @classmethod
    def new_in_date_range(cls, date_range: DateRange):
        return cls(start=date_range.start, stop=date_range.end)

    @property
    def time_delta(self):
        """Get event time delta (minutes)."""
        delta = self.stop - self.start
        minutes_count = round(delta.total_seconds() / 60, 2)
        return minutes_count


class EventEntity(UUIDLabelEntity, TimeRangeEntity):
    """EventEntity to follow exchange of Resource between Agent."""

    class Meta:
        abstract = True


class AgentEntity(UUIDLabelEntity):
    """An agent can be people or human agencies."""

    class Meta:
        abstract = True
        verbose_name = _("Agent")
        verbose_name_plural = _("Agent(s)")

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self._meta.model_name}: {self.user.get_username()}"


class ResourceEntity(UUIDLabelEntity):
    """A resource is something you need, and you may use to achieve.

    Resource can be reserved or used by and Event.
    """

    class Meta:
        abstract = True

    value = models.DecimalField(
        verbose_name=_("Resource value"),
        default=Deci(0.0),
        max_digits=18,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.short_prefix_uuid}: {self.value}"
