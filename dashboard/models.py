from django.db import models
from django.contrib.auth.models import AbstractUser


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('conference', 'Conférence'),
        ('workshop', 'Atelier'),
        ('cultural', 'Culturel'),
        ('ftour', 'Ftour'),
        ('competition', 'Compétition'),
        ('charity', 'Caritatif'),
        ('talent_show', 'Eigsi Got Talent'),
        ('integration_day', 'Journée d\'intégration'),
        ('other', 'Autres'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, verbose_name="Type d'évènement")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    date = models.DateTimeField(verbose_name="Date de l'évènement")
    organizer = models.CharField(max_length=100, verbose_name="Organisateur")
    is_public = models.BooleanField(default=True, verbose_name="Public ?")
    status = models.BooleanField(default=False, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    archived_at = models.DateTimeField(null=True, verbose_name="Archivé le")
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name="Affiche de l'évènement")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Évènement"
        verbose_name_plural = "Évènements"
        ordering = ['-date']


class EventGallery(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name="Événement"
    )
    image = models.ImageField(
        upload_to='galleries/',
        verbose_name="Image"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Légende"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )

    class Meta:
        verbose_name = "Image de la galerie"
        verbose_name_plural = "Images de la galerie"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image pour {self.event.title}"