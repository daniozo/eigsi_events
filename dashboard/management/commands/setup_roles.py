from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from dashboard.models import Event

class Command(BaseCommand):
    help = "Set up user roles and permissions"

    def handle(self, *args, **options):
        # Define groupes
        guest_group, created = Group.objects.get_or_create(name='Guest')
        student_group, created = Group.objects.get_or_create(name='Student')
        admin_group, created = Group.objects.get_or_create(name='Admin')
        super_admin_group, created = Group.objects.get_or_create(name='SuperAdmin')

        # Get basic permissions on the Event model
        content_type = ContentType.objects.get_for_model(Event)
        view_event_permission = Permission.objects.get(codename='view_event', content_type=content_type)
        add_event_permission = Permission.objects.get(codename='add_event', content_type=content_type)
        change_event_permission = Permission.objects.get(codename='change_event', content_type=content_type)
        delete_event_permission = Permission.objects.get(codename='delete_event', content_type=content_type)

        # Assign permissions to groups
        guest_group.permissions.add(view_event_permission)
        student_group.permissions.add(view_event_permission)
        admin_group.permissions.add(view_event_permission, add_event_permission, change_event_permission)
        super_admin_group.permissions.add(view_event_permission, add_event_permission, change_event_permission, delete_event_permission)

        self.stdout.write(self.style.SUCCESS("Roles and permissions set up successfully"))
