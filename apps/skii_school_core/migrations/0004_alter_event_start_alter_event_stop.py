# Generated by Django 4.2.4 on 2023-08-12 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("skii_school_core", "0003_remove_companyagent_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="start",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 12, 21, 24, 57, 500809, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Start time",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="stop",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 12, 21, 24, 57, 500823, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Stop time",
            ),
        ),
    ]
