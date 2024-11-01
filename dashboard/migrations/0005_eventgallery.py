# Generated by Django 5.1.1 on 2024-10-28 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_event_poster"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventGallery",
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
                    "image",
                    models.ImageField(upload_to="galleries/", verbose_name="Image"),
                ),
                (
                    "caption",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="Légende"
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date d'ajout"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery",
                        to="dashboard.event",
                        verbose_name="Événement",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image de la galerie",
                "verbose_name_plural": "Images de la galerie",
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
