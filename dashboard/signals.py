from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
import uuid


@receiver(pre_save, sender=SocialAccount)
def prepare_user(sender, instance, **kwargs):
    print("Signal `pre_save` de SocialAccount déclenché")
    if instance.pk is None and instance.provider == 'google':
        user = instance.user
        extra_data = instance.extra_data

        google_first_name = extra_data.get('given_name', '')
        google_last_name = extra_data.get('family_name', '')
        google_email = extra_data.get('email', '')

        if google_email:
            base_username = google_email.split('@')[0]
        else:
            base_username = f"user_{str(uuid.uuid4())[:8]}"

        if not base_username or base_username.isspace():
            base_username = f"user_{str(uuid.uuid4())[:8]}"

        unique_username = base_username
        counter = 1
        while User.objects.filter(username=unique_username).exists() or not unique_username:
            unique_username = f"{base_username}_{counter}"
            counter += 1

        print(f"Username généré : {unique_username}")

        user.username = unique_username
        user.first_name = google_first_name if google_first_name else unique_username
        user.last_name = google_last_name if google_last_name else ''

        if google_email and not user.email:
            user.email = google_email

        try:
            user.save()
            print(f"Utilisateur {user.username} mis à jour avec succès")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'utilisateur : {str(e)}")


@receiver(post_save, sender=SocialAccount)
def setup_user_groups(sender, instance, created, **kwargs):
    if created and instance.provider == 'google':
        user = instance.user
        student_group, _ = Group.objects.get_or_create(name='Student')

        if not user.groups.filter(name__in=['Admin', 'SuperAdmin']).exists():
            user.groups.add(student_group)
            print(f"User {user.username} has been added to the Student group")
        else:
            print(f"User {user.username} is already in another group")

        # Verify and mark the email as verified
        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={'verified': True, 'primary': True}
        )