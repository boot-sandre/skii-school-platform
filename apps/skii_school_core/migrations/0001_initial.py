# Generated by Django 4.2.4 on 2023-08-12 20:45

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CurrencyRessource",
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
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=3, unique=True)),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "values",
                    models.DecimalField(
                        decimal_places=3,
                        default=Decimal("1"),
                        max_digits=5,
                        verbose_name="Price factor against dollars",
                    ),
                ),
            ],
            options={
                "verbose_name": "Currency",
                "verbose_name_plural": "Currency(s)",
            },
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(default="New events", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="WorktimeRessource",
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
                    "name",
                    models.CharField(default="New work time ressource", max_length=255),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "time_elasped",
                    models.FloatField(default=0.0, verbose_name="Work time (seconds)"),
                ),
                (
                    "time_planned",
                    models.FloatField(
                        default=600.0, verbose_name="Time planned (seconds)"
                    ),
                ),
            ],
            options={
                "verbose_name": "Worktime",
                "verbose_name_plural": "Worktime(s)",
            },
        ),
        migrations.CreateModel(
            name="TeacherAgent",
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
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Teacher",
                "verbose_name_plural": "Teachers",
            },
        ),
        migrations.CreateModel(
            name="StudentAgent",
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
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Student",
                "verbose_name_plural": "Students",
            },
        ),
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(default="New events", max_length=255)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("planned", "Planned"),
                            ("in_progress", "In progress"),
                            ("cancelled", "Cancelled"),
                            ("postponed", "Postponed in time"),
                            ("finished", "finished"),
                        ],
                        default="draft",
                        max_length=128,
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(auto_now_add=True, verbose_name="Start time"),
                ),
                (
                    "stop",
                    models.DateTimeField(auto_now_add=True, verbose_name="Stop time"),
                ),
                (
                    "agent_invited",
                    models.ManyToManyField(
                        blank=True, related_name="events", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user_creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Event(s)",
            },
        ),
        migrations.CreateModel(
            name="CompanyAgent",
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
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "last_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Last Modified"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
            },
        ),
    ]
