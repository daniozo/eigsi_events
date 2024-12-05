import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = "Load users data into the database"

    def handle(self, *args, **kwargs):
       
        groups = list(Group.objects.all())
        student_group = None

        for g in groups:
            if g.name == "Guest":
                student_group = g
                break

        if not student_group:
            print("Le groupe 'Guest' n'existe pas.")
        else:
            def generate_last_name():
                last_names = ["John", "Jane", "Jim", "Jill", "Bob", "Bobby",
                            "Alice", "Alicia", "Tom", "Tina"]
                return random.choice(last_names)

            def generate_first_name():
                first_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones",
                            "Garcia", "Miller", "Davis", "Martinez"]
                return random.choice(first_names)

            def generate_email():
                domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"]
                username = f"{generate_first_name()}.{generate_last_name()}_{random.randint(1, 99)}"
                return f"{username}@{random.choice(domains)}"

            for i in range(15):
                first_name = generate_first_name()
                last_name = generate_last_name()
                email = generate_email()
                username = f"{first_name.lower()}.{last_name.lower()}_{i}"
                password = "default_password"

                user = User.objects.create_user(username=username, first_name=first_name,
                                                last_name=last_name, email=email, password=password)

                student_group.user_set.add(user)

            print("15 utilisateurs ont été créés et ajoutés au groupe 'Guest'.")