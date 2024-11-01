# Generated by Django 5.1.1 on 2024-10-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_event_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="poster",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="posters/",
                verbose_name="Affiche de l'évènement",
            ),
        ),
    ]