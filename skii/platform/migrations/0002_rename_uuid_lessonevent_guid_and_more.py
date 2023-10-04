# Generated by Django 4.2.5 on 2023-09-28 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("platform", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lessonevent",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="locationresource",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="moneyresource",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="studentagent",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="teacheragent",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="timeresource",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="visualalbum",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="visualelement",
            old_name="uuid",
            new_name="guid",
        ),
        migrations.RenameField(
            model_name="visualpicture",
            old_name="uuid",
            new_name="guid",
        ),
    ]
