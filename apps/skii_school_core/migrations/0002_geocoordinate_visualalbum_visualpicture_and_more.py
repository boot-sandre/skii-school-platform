# Generated by Django 4.2.4 on 2023-03-31 02:07

import apps.skii_school_core.entities
import apps.skii_school_core.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("skii_school_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GeoCoordinate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        decimal_places=4,
                        max_digits=6,
                        validators=[
                            django.core.validators.MaxValueValidator(limit_value=90),
                            django.core.validators.MinValueValidator(limit_value=-90),
                        ],
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        decimal_places=4,
                        max_digits=7,
                        validators=[
                            django.core.validators.MaxValueValidator(limit_value=180),
                            django.core.validators.MinValueValidator(limit_value=-180),
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name": "Geographic coordinate",
                "verbose_name_plural": "Geographic coordinate(s)",
                "ordering": ["latitude", "longitude"],
            },
        ),
        migrations.CreateModel(
            name="VisualAlbum",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Short description",
                    ),
                ),
                (
                    "title",
                    models.CharField(default="", max_length=255, verbose_name="Title"),
                ),
            ],
            options={
                "verbose_name": "Visual Album",
                "verbose_name_plural": "Visual Album(s)",
                "ordering": ["-last_modified", "-created", "title"],
            },
        ),
        migrations.CreateModel(
            name="VisualPicture",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Short description",
                    ),
                ),
                (
                    "title",
                    models.CharField(default="", max_length=255, verbose_name="Title"),
                ),
                (
                    "picture",
                    models.ImageField(
                        default=apps.skii_school_core.entities.get_default_cover_image,
                        upload_to="",
                        verbose_name="Picture",
                    ),
                ),
            ],
            options={
                "verbose_name": "Visual Picture",
                "verbose_name_plural": "Visual Picture(s)",
                "ordering": ["-last_modified", "-created", "title"],
            },
        ),
        migrations.AlterModelOptions(
            name="event",
            options={
                "ordering": ["state", "-created", "-start", "-stop", "title"],
                "verbose_name": "Event",
                "verbose_name_plural": "Event(s)",
            },
        ),
        migrations.AlterModelOptions(
            name="location",
            options={
                "ordering": ["-last_modified", "-created", "country", "city", "label"],
                "verbose_name": "Location",
                "verbose_name_plural": "Location(s)",
            },
        ),
        migrations.AlterModelOptions(
            name="studentagent",
            options={
                "ordering": ["-last_modified", "-created", "user__username"],
                "verbose_name": "Student",
                "verbose_name_plural": "Student(s)",
            },
        ),
        migrations.AlterModelOptions(
            name="teacheragent",
            options={
                "ordering": ["-last_modified", "-created", "user__username"],
                "verbose_name": "Teacher",
                "verbose_name_plural": "Teacher(s)",
            },
        ),
        migrations.RenameField(
            model_name="moneyressource",
            old_name="description_short",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="timeressource",
            old_name="description_short",
            new_name="description",
        ),
        migrations.RemoveField(
            model_name="event",
            name="label",
        ),
        migrations.AddField(
            model_name="event",
            name="title",
            field=models.CharField(default="", max_length=255, verbose_name="Title"),
        ),
        migrations.AddField(
            model_name="location",
            name="content",
            field=models.TextField(
                blank=True, null=True, verbose_name="Full content to display"
            ),
        ),
        migrations.AddField(
            model_name="moneyressource",
            name="label",
            field=models.CharField(default="", max_length=255, verbose_name="Label"),
        ),
        migrations.AddField(
            model_name="timeressource",
            name="label",
            field=models.CharField(default="", max_length=255, verbose_name="Label"),
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Short description"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="country",
            field=django_countries.fields.CountryField(
                default="RO", max_length=2, verbose_name="Country"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="description",
            field=models.TextField(
                blank=True, max_length=255, null=True, verbose_name="Short description"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="label",
            field=models.CharField(default="", max_length=255, verbose_name="Label"),
        ),
        migrations.CreateModel(
            name="VisualElement",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Short description",
                    ),
                ),
                (
                    "title",
                    models.CharField(default="", max_length=255, verbose_name="Title"),
                ),
                (
                    "picture",
                    models.ImageField(
                        default=apps.skii_school_core.entities.get_default_cover_image,
                        upload_to="",
                        verbose_name="Picture",
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        default=apps.skii_school_core.models.get_default_album,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="skii_school_core.visualalbum",
                        verbose_name="Album",
                    ),
                ),
            ],
            options={
                "verbose_name": "Visual Album Picture",
                "verbose_name_plural": "Visual Album Picture(s)",
                "ordering": ["-last_modified", "-created", "title"],
            },
        ),
        migrations.AddField(
            model_name="location",
            name="coordinate",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="skii_school_core.geocoordinate",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="cover",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="skii_school_core.visualpicture",
            ),
        ),
        migrations.AddField(
            model_name="location",
            name="illustration",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="skii_school_core.visualalbum",
            ),
        ),
    ]