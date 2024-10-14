# Generated by Django 5.1.1 on 2024-10-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
                    "event_type",
                    models.CharField(
                        choices=[
                            ("conference", "Conférence"),
                            ("workshop", "Atelier"),
                            ("cultural", "Culturel"),
                            ("iftar", "Ftour"),
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
                    "organizer",
                    models.CharField(max_length=100, verbose_name="Organisateur"),
                ),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="Public ?"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Créé le"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Mis à jour le"),
                ),
            ],
            options={
                "verbose_name": "Évènement",
                "verbose_name_plural": "Évènements",
                "ordering": ["-date"],
            },
        ),
    ]
