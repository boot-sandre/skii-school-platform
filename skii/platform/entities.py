import uuid
from decimal import Decimal as Deci

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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def short_prefix_uuid(self):
        """Usefull for have short uuid preview."""
        return f"{str(self.uuid)[:8]}..."


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


class EventEntity(UUIDLabelEntity):
    """EventEntity to follow exchange of Resource between Agent."""

    class Meta:
        abstract = True

    start = models.DateTimeField(verbose_name=_("Start time"), default=now)
    stop = models.DateTimeField(verbose_name=_("Stop time"), default=now)

    @property
    def time_delta(self):
        """Get event time delta (minutes)."""
        delta = self.stop - self.start
        minutes_count = round(delta.total_seconds() / 60, 2)
        return minutes_count


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
