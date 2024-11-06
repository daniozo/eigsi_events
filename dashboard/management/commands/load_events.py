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
                "title": "Conférence IA et Big Data",
                "description": "Une conférence dédiée aux avancées récentes en intelligence artificielle et big data.",
                "event_type": "conference",
                "location": "Amphithéâtre Principal",
                "date": timezone.datetime(2024, 11, 10, 14, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Hackathon Énergie Verte",
                "description": "Un hackathon pour développer des solutions énergétiques renouvelables.",
                "event_type": "competition",
                "location": "Salle de conférences A",
                "date": timezone.datetime(2024, 11, 20, 8, 0),
                "is_public": False,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Atelier de Programmation en Python",
                "description": "Formation pour les débutants en programmation Python.",
                "event_type": "workshop",
                "location": "Laboratoire Informatique 3",
                "date": timezone.datetime(2024, 11, 25, 16, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Journée Carrière",
                "description": "Rencontres avec des entreprises pour explorer des opportunités de stage et d'emploi.",
                "event_type": "other",
                "location": "Salle Polyvalente",
                "date": timezone.datetime(2024, 11, 28, 9, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Atelier de Conception Web",
                "description": "Découverte des principes de design web et des outils modernes.",
                "event_type": "workshop",
                "location": "Laboratoire Informatique 1",
                "date": timezone.datetime(2024, 12, 3, 10, 0),
                "is_public": False,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Festival Culturel International",
                "description": "Une journée pour découvrir les cultures du monde à travers des stands et des spectacles.",
                "event_type": "cultural",
                "location": "Parc du Campus",
                "date": timezone.datetime(2024, 12, 8, 11, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Séance de Ftour Collectif",
                "description": "Rassemblement convivial pour un ftour en famille et entre amis.",
                "event_type": "ftour",
                "location": "Jardin de la Résidence",
                "date": timezone.datetime(2024, 12, 15, 18, 30),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Compétition de Robotique",
                "description": "Affrontez d'autres équipes dans des défis de robotique variés.",
                "event_type": "competition",
                "location": "Salle Polytechnique",
                "date": timezone.datetime(2025, 1, 10, 9, 30),
                "is_public": True,
                "status": False,
                "poster": random.choice(posters)
            },
            {
                "title": "Gala Caritatif de Fin d'Année",
                "description": "Une soirée de bienfaisance pour lever des fonds pour des œuvres sociales.",
                "event_type": "charity",
                "location": "Salle de Bal",
                "date": timezone.datetime(2025, 1, 20, 19, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Conférence sur les Énergies Renouvelables",
                "description": "Présentation des dernières avancées dans le domaine des énergies vertes.",
                "event_type": "conference",
                "location": "Amphithéâtre 2",
                "date": timezone.datetime(2025, 2, 15, 10, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            },
            {
                "title": "Eigsi Got Talent",
                "description": "Concours de talents ouvert aux étudiants : chant, danse, magie, etc.",
                "event_type": "talent_show",
                "location": "Auditorium Principal",
                "date": timezone.datetime(2025, 3, 5, 18, 0),
                "is_public": True,
                "status": False,
                "poster": random.choice(posters)
            },
            {
                "title": "Journée d'Intégration des Nouveaux Étudiants",
                "description": "Activités et jeux pour accueillir et intégrer les nouveaux venus.",
                "event_type": "integration_day",
                "location": "Complexe Sportif",
                "date": timezone.datetime(2025, 3, 10, 14, 0),
                "is_public": True,
                "status": True,
                "poster": random.choice(posters)
            }
        ]

        for event_data in events:
            Event.objects.create(**event_data)

        self.stdout.write(self.style.SUCCESS("Les événements ont été ajoutés à la base de données avec succès !"))
