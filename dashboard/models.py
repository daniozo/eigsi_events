from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
    poster = models.ImageField(upload_to='posters/', null=True, blank=True, verbose_name="Affiche de l'évènement")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, verbose_name="Type d'évènement")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    date = models.DateTimeField(verbose_name="Date de l'évènement")
    is_public = models.BooleanField(default=True, verbose_name="Public ?")
    price = models.TextField(null=True, verbose_name="Prix")
    status = models.BooleanField(default=False, verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    archived_at = models.DateTimeField(null=True, verbose_name="Archivé le")

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


class Operation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    type = models.CharField(max_length=25, verbose_name="Type d'opération")
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Réalisé le")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Titre de l'élément") #used when content was deleted

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Opération"
        verbose_name_plural = "Opérations"
        ordering = ['-date_time']


class Guest(AbstractUser):
    status = models.TextField(max_length=100, verbose_name="Status")
    origin = models.TextField(max_length=200, verbose_name="Origin")
    groups = models.ManyToManyField(Group, related_name="guest_group", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="guest_user_permissions", blank=True)


class Participation(models.Model):
    RATING_CHOICES = [
        (1, '1 étoile'),
        (2, '2 étoiles'),
        (3, '3 étoiles'),
        (4, '4 étoiles'),
        (5, '5 étoiles'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name="Événement"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='participations',
        verbose_name="Utilisateur"
    )

    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='participations',
        verbose_name="Invité"
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        verbose_name="Note"
    )

    is_registered = models.BooleanField(
        default=False,
        verbose_name="Est inscrit à l'évènement"
    )

    is_pending = models.BooleanField(
        default=True,
        verbose_name="En attente de validation"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le"
    )

    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Mise à jour le"
    )

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = [['event', 'user'], ['event', 'guest']]

    def clean(self):
        if self.user and self.guest:
            raise ValidationError("Une participation ne peut pas avoir à la fois un utilisateur et un invité")
        if not self.user and not self.guest:
            raise ValidationError("Une participation doit avoir soit un utilisateur soit un invité")

    def __str__(self):
        participant = self.user if self.user else self.guest
        return f"Participation de {participant} à {self.event}"