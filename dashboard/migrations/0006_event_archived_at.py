# Generated by Django 5.1.1 on 2024-10-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_eventgallery"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="archived_at",
            field=models.DateTimeField(null=True, verbose_name="Archivé le"),
        ),
    ]
