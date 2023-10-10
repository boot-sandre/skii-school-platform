import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from decimal import Decimal as Deci
from numbers import Number
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
class DatetimeRange:
    """
    Represents a date range with a start and stop date.

    Args:
        start (datetime): The start date and time of the range.
        stop (datetime): The stop date and time of the range.

    Raises:
        ValueError: If the stop date is not later than the start date.
        ValueError: If ones of start/stop attribut is not datetime aware.

    Attributes:
        start (datetime): The start date and time of the range.
        stop (datetime): The stop date and time of the range.
    """

    start: datetime
    stop: datetime

    def __post_init__(self) -> None:
        self.validate_start_before_stop()
        self.validate_timezone_aware()

    def validate_timezone_aware(self):
        """ Validates that datetime used for attribut start/stop is timezone aware.

            Raises:
                ValueError: If ones of start/stop attribut is not datetime aware.
        """
        if not self.start.tzinfo or not self.stop.tzinfo:
            raise ValueError(f"Datetime is not timezone aware ({self.start, self.stop}).")

    def validate_start_before_stop(self):
        """ Validates that the stop date is later than the start date.

            Raises:
                ValueError: If the start date is not later than the stop date.
        """
        if self.start >= self.stop:
            raise ValueError("Cannot stop before starting.")

    def __str__(self) -> str:
        """
        Returns a string representation of the TimeRange.

        Returns:
            str: A string representation of the TimeRange
                 with start/stop/duration(minutes)
        """
        return f"{self.start} - {self.stop} so {self.duration} minutes"

    def __add__(self, other: timedelta) -> "DatetimeRange":
        """
        Adds a timedelta to the start and stop dates of the DatetimeRange.

        Args:
            other (timedelta): The timedelta to add to the DatetimeRange.

        Returns:
            DatetimeRange: A new DatetimeRange with adjusted start and stop dates.

        Raises:
            TypeError: If the provided argument is not a timedelta.
        """
        if isinstance(other, timedelta):
            return DatetimeRange(self.start + other, self.stop + other)

        raise TypeError()

    def hour_later(self) -> "DatetimeRange":
        """
        Returns DatetimeRange with both start and stop dates shifted by one hour later.

        Returns:
            DatetimeRange: A new DatetimeRange with adjusted start and stop dates.
        """
        return self + timedelta(hours=1)

    @property
    def delta(self) -> timedelta:
        return self.stop - self.start

    @property
    def duration(self) -> int:
        """
        Calculates the duration of the DatetimeRange.

        Returns:
            timedelta: The duration between the start and stop dates.
        """
        return round((self.stop - self.start).seconds / 60)

    def overlaps(self, datetime_range: "DatetimeRange") -> bool:
        """
        Checks if the DatetimeRange overlaps with another DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange to check for overlap with.

        Returns:
            bool: True if there is overlap, False otherwise.
        """
        return self.start <= datetime_range.stop and self.stop >= datetime_range.start

    def starts_before(self, datetime_range: "DatetimeRange") -> bool:
        """
        Checks if the DatetimeRange starts before another DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange to compare with.

        Returns:
            bool: True if the DatetimeRange starts before the other DatetimeRange,
                False otherwise.
        """
        return self.start < datetime_range.start

    def range(self, step: timedelta) -> Iterator[datetime]:
        """
        Get Sequence of datetimes within the DatetimeRange with a specified time step.

        Args:
            step (timedelta): The time step between generated datetimes.

        Yields:
            datetime: Datetimes within the DatetimeRange at specified intervals.
        """
        current_datetime = self.start
        while current_datetime < self.stop:
            yield current_datetime
            current_datetime = current_datetime + step

    def is_contained_or_equal(self, other: "DatetimeRange") -> bool:
        """
        Check if this DatetimeRange is contained within or equal to another DatetimeRange.

        Args:
            other (DatetimeRange): The other DatetimeRange to compare with.

        Returns:
            bool: True if this DatetimeRange is contained within or equal to the other DatetimeRange,
                  False otherwise.
        """
        return self.start >= other.start and self.stop <= other.stop

    def is_contained_or_equal_daytime(self, other: "TimeRange") -> bool:
        """
        Check if this DatetimeRange is contained within or equal to a TimeRange.

        Args:
            other (DatetimeRange): The other DatetimeRange to compare with.

        Returns:
            bool: True if this DatetimeRange is contained within or equal to the other DatetimeRange,
                  False otherwise.
        """
        return self.start >= other.start and self.stop <= other.stop

    @classmethod
    def to_date_time(cls, datetime_range: "DatetimeRange") -> "TimeRange":
        """
        Create a TimeRange from a DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange to convert.

        Returns:
            TimeRange: The equivalent TimeRange with start and stop times.
        """
        start_time = datetime_range.start.time()
        stop_time = datetime_range.stop.time()

        return cls(start_time, stop_time)


@dataclass(frozen=True)
class TimeRange:
    """
    Represents a time range with a start and stop time.

    Args:
        start (time): The start time of the range.
        stop (time): The stop time of the range.

    Raises:
        ValueError: If the stop time is not later than the start time.
    """

    start: time
    stop: time

    def __post_init__(self) -> None:
        """
        Validates that the stop time is later than the start time.

        Raises:
            ValueError: If the stop time is not later than the start time.
        """
        if self.start >= self.stop:
            raise ValueError("Can not stop before starting.")

    def __str__(self) -> str:
        """
        Returns a string representation of the TimeRange.

        Returns:
            str: A string representation of the TimeRange.
        """
        return f"{self.start} - {self.stop} so {self.duration} minutes"

    def __add__(self, other: int) -> "TimeRange":
        """
        Adds a specified number of minutes to both start and stop times.

        Args:
            other (int): The number of minutes to add to the TimeRange.

        Returns:
            TimeRange: A new TimeRange with adjusted start and stop times.

        Raises:
            TypeError: If the provided argument is not an integer.
        """
        if isinstance(other, int):
            new_start = self.start.replace(minute=self.start.minute + other)
            new_stop = self.stop.replace(minute=self.stop.minute + other)
            return TimeRange(new_start, new_stop)

        raise TypeError()

    @property
    def delta(self) -> timedelta:
        return time_to_timedelta(self.start, self.stop)

    @property
    def duration(self) -> int:
        """
        Calculates the duration of the TimeRange in minutes.

        Returns:
            int: The duration between the start and stop times in minutes.
        """
        return round(self.delta.total_seconds / 60)

    def overlaps(self, time_range: "TimeRange") -> bool:
        """
        Checks if the TimeRange overlaps with another TimeRange.

        Args:
            time_range (TimeRange): The TimeRange to check for overlap with.

        Returns:
            bool: True if there is overlap, False otherwise.
        """
        return self.start <= time_range.stop and self.stop >= time_range.start

    def starts_before(self, time_range: "TimeRange") -> bool:
        """
        Checks if the TimeRange starts before another TimeRange.

        Args:
            time_range (TimeRange): The TimeRange to compare with.

        Returns:
            bool: True if the TimeRange starts before the other TimeRange,
                  False otherwise.
        """
        return self.start < time_range.start

    def time_range(self) -> "TimeRange":
        """
        Returns the TimeRange as is.

        Returns:
            TimeRange: The TimeRange itself.
        """
        return self

    def is_contained_or_equal(self, other: "TimeRange") -> bool:
        """
        Check if this TimeRange is completely contained within or equal to another TimeRange.

        Args:
            other (TimeRange): The other TimeRange to compare with.

        Returns:
            bool: True if this TimeRange is completely contained within or equal to the other TimeRange,
                  False otherwise.
        """
        return self.start >= other.start and self.stop <= other.stop

    @classmethod
    def from_datetime_range(cls, datetime_range: DatetimeRange) -> "TimeRange":
        """
        Create a TimeRange from a DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange to convert.

        Returns:
            TimeRange: The equivalent TimeRange with start and stop times.
        """
        # Extract the time components (hours and minutes) from the start and stop datetime
        start_time = datetime_range.start.timetz()
        stop_time = datetime_range.stop.timetz()

        return cls(start_time, stop_time)


class DatetimeRangeQueryset(models.QuerySet):
    """
    A custom queryset for querying objects with time ranges.

    Attributes:
        model: The model to which this queryset belongs.
        using: The database alias to use for the queryset.
    """

    def filter(self, *args, **kwargs):
        """
        Filters the queryset based on a DatetimeRange.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Keyword Args:
            datetime_range (DatetimeRange): The DatetimeRange for filtering.

        Returns:
            QuerySet: A filtered queryset.
        """
        datetime_range = kwargs.get("datetime_range")

        if datetime_range and isinstance(datetime_range, DatetimeRange):
            kwargs["start"] = datetime_range.start
            kwargs["stop"] = datetime_range.stop

        return super().filter(*args, **kwargs)

    def filter_by_time_interval(self, time_interval):
        """
        Filter events based on a TimeInterval.

        Args:
            time_interval (TimeInterval): The TimeInterval for filtering.

        Returns:
            QuerySet: A filtered queryset.
        """
        return self.filter(
            start_time__time__gte=time_interval.start_time,
            stop_time__time__lte=time_interval.stop_time,
        )

    def filter_by_start_time_in_interval(self, time_interval):
        """
        Filter events whose start time is within the TimeInterval.

        Args:
            time_interval (TimeInterval): The TimeInterval for filtering.

        Returns:
            QuerySet: A filtered queryset.
        """
        return self.filter(
            start_time__time__gte=time_interval.start_time,
            start_time__time__lte=time_interval.stop_time,
        )

    def filter_by_stop_time_in_interval(self, time_interval):
        """
        Filter events whose stop time is within the TimeInterval.

        Args:
            time_interval (TimeInterval): The TimeInterval for filtering.

        Returns:
            QuerySet: A filtered queryset.
        """
        return self.filter(
            stop_time__time__gte=time_interval.start_time,
            stop_time__time__lte=time_interval.stop_time,
        )


class TimeRangeManager(models.Manager):
    """
    A custom manager for objects with time ranges.

    Attributes:
        model: The model to which this manager belongs.
    """

    def get_queryset(self):
        """
        Get the custom queryset for this manager.

        Returns:
            DatetimeRangeQueryset: The custom queryset.
        """
        return DatetimeRangeQueryset(self.model, using=self._db)

    def in_range(self, datetime_range: DatetimeRange):
        """
        Filter objects that are within the specified DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange for filtering.

        Returns:
            QuerySet: A filtered queryset containing objects within the DatetimeRange.
        """
        return self.get_queryset().filter(
            start__gte=datetime_range.start, stop__lte=datetime_range.stop
        )


class DatetimeRangeEntity(models.Model):
    """
    An abstract base class representing an entity with a time range.

    Attributes:
        start (datetime): The start date and time of the time range.
        stop (datetime): The stop date and time of the time range.
    """

    class Meta:
        abstract = True

    start = models.DateTimeField(verbose_name=_("Start time"), default=now)
    stop = models.DateTimeField(verbose_name=_("Stop time"), default=now)

    objects = TimeRangeManager()

    @property
    def datetime_range(self) -> DatetimeRange:
        """
        Get the time range as a DatetimeRange instance.

        Returns:
            DatetimeRange: A DatetimeRange representing the time range.
        """
        return DatetimeRange(self.start, self.stop)

    @datetime_range.setter
    def datetime_range(self, value: DatetimeRange) -> None:
        """
        Set the time range using a DatetimeRange instance.

        Args:
            value (DatetimeRange): The DatetimeRange to set
        """
        self.start = value.start
        self.stop = value.stop

    @classmethod
    def new_in_datetime_range(cls, datetime_range: DatetimeRange):
        """
        Create a new instance within the specified DatetimeRange.

        Args:
            datetime_range (DatetimeRange): The DatetimeRange in which to create the instance.

        Returns:
            DatetimeRangeEntity: A new instance with start and stop times
                matching the DatetimeRange.
        """
        return cls(start=datetime_range.start, stop=datetime_range.stop)

    def __str__(self) -> str:
        start_datetime = self.start.strftime("%Y-%m-%d %H:%M")
        stop_datetime = self.stop.strftime("%Y-%m-%d %H:%M")
        return (
            f"{start_datetime} to {stop_datetime} so {self.time_delta_minutes} minutes"
        )

    @property
    def time_delta_minutes(self):
        """Get event time delta (minutes)."""
        delta = self.stop - self.start
        minutes_count = round(delta.total_seconds() / 60, 2)
        return minutes_count


class EventEntity(UUIDLabelEntity, DatetimeRangeEntity):
    """EventEntity to follow exchange of Resource between Agent."""

    class Meta:
        abstract = True


class AgentEntity(UUIDLabelEntity):
    """An agent can be people or human agencies."""

    class Meta:
        abstract = True
        verbose_name = _("Agent")
        verbose_name_plural = _("Agent(s)")

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, limit_choices_to={"is_active": True}
    )

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


def time_to_timedelta(start_time: time, end_time: time) -> timedelta:
    """
    Calculate the timedelta between two time objects, considering midnight.

    Args:
        start_time (datetime.time): The starting time.
        end_time (datetime.time): The ending time.

    Returns:
        datetime.timedelta: The timedelta representing the difference
        between the two time objects.

    Example:
        >>> start = time(23, 0)  # 11:00 PM
        >>> end = time(1, 30)    # 1:30 AM (next day)
        >>> time_difference_to_timedelta(start, end)
        datetime.timedelta(seconds=9000)  # 2 hours and 30 minutes
    """
    # Create datetime objects for today and tomorrow
    today = datetime.today()
    tomorrow = today + timedelta(days=1)

    # Combine the date with the time objects
    start_datetime = datetime.combine(today, start_time)
    end_datetime = datetime.combine(today, end_time)

    # Check if the end time is before the start time (crosses midnight)
    if end_time < start_time:
        end_datetime = datetime.combine(tomorrow, end_time)

    # Calculate the timedelta
    time_difference = end_datetime - start_datetime

    return time_difference
