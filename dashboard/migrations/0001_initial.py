# Generated by Django 5.1.1 on 2024-11-06 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ("title", models.CharField(max_length=200, verbose_name="Titre")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="posters/",
                        verbose_name="Affiche de l'évènement",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("conference", "Conférence"),
                            ("workshop", "Atelier"),
                            ("cultural", "Culturel"),
                            ("ftour", "Ftour"),
                            ("competition", "Compétition"),
                            ("charity", "Caritatif"),
                            ("talent_show", "Eigsi Got Talent"),
                            ("integration_day", "Journée d'intégration"),
                            ("other", "Autres"),
                        ],
                        max_length=20,
                        verbose_name="Type d'évènement",
                    ),
                ),
                ("location", models.CharField(max_length=200, verbose_name="Lieu")),
                ("date", models.DateTimeField(verbose_name="Date de l'évènement")),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="Public ?"),
                ),
                ("status", models.BooleanField(default=False, verbose_name="Statut")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Créé le"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Mis à jour le"),
                ),
                (
                    "archived_at",
                    models.DateTimeField(null=True, verbose_name="Archivé le"),
                ),
            ],
            options={
                "verbose_name": "Évènement",
                "verbose_name_plural": "Évènements",
                "ordering": ["-date"],
            },
        ),
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
        migrations.CreateModel(
            name="Operation",
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
                    "type",
                    models.CharField(max_length=25, verbose_name="Type d'opération"),
                ),
                (
                    "date_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Réalisé le"),
                ),
                ("object_id", models.PositiveIntegerField(null=True)),
                (
                    "content_title",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Titre de l'élément",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur",
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Opération",
                "verbose_name_plural": "Opérations",
                "ordering": ["-date_time"],
            },
        ),
    ]
