import random
from django.core.management.base import BaseCommand
from dashboard.models import Event
from django.utils import timezone

class Command(BaseCommand):
    help = "Load events data into the database"

    def handle(self, *args, **kwargs):
        posters = [
            "posters/eigsi_event_default_banner.png",
            "posters/img_3u4Wk4e.png",
            "posters/133695436347860455_uTgc7b0.jpg",
            "posters/133683029759907961_Le4bCF7.jpg",
            "posters/133695436347860455_GmNV8mD.jpg",
            "posters/133695436347860455_VW7WLO7.jpg"
        ]

        events = [
            {
                "title": "Cérémonie Culturelle des Étudiants",
                "description": "Une soirée culturelle organisée par les étudiants du campus.",
                "event_type": "cultural",
                "location": "Salon des Festivals",
                "date": timezone.datetime(2024, 11, 15, 18, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Ftour Étudiant de la Semaine",
                "description": "Un week-end dédié aux étudiants avec des activités culturelles, sportives et récréatives.",
                "event_type": "ftour",
                "location": "Campus Entire",
                "date": timezone.datetime(2024, 11, 25, 9, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Compétition de Cuisine",
                "description": "Une compétition de cuisine entre les étudiants pour le meilleur plat français.",
                "event_type": "competition",
                "location": "Salle des Conférences B",
                "date": timezone.datetime(2024, 11, 30, 15, 0),
                "is_public": False,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Caritatif du Campus",
                "description": "Une journée de bénévolat pour les œuvres caritables locales.",
                "event_type": "charity",
                "location": "Campus Entire",
                "date": timezone.datetime(2024, 12, 2, 9, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Eigsi Got Talent",
                "description": "Un concours de talent pour les étudiants du campus.",
                "event_type": "talent_show",
                "location": "Salle des Festivals",
                "date": timezone.datetime(2024, 12, 5, 16, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Journée d'Intégration des Nouveaux Étudiants",
                "description": "Une journée dédiée aux nouveaux arrivants pour les aider à s'intégrer au campus.",
                "event_type": "integration_day",
                "location": "Salon des Festivals",
                "date": timezone.datetime(2024, 11, 7, 9, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Conférence sur la Durabilité Économique",
                "description": "Une conférence sur les défis et opportunités de l'économie durable.",
                "event_type": "conference",
                "location": "Amphithéâtre Principal",
                "date": timezone.datetime(2024, 11, 18, 14, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Atelier de Graphisme pour les Designers",
                "description": "Un atelier sur la création et le rendu des designs graphiques.",
                "event_type": "workshop",
                "location": "Salle des Ateliers",
                "date": timezone.datetime(2024, 11, 3, 10, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
        ]

        for event_data in events:
            Event.objects.create(**event_data)

        self.stdout.write(self.style.SUCCESS("Les événements ont été ajoutés à la base de données avec succès !"))
