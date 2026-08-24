import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates or promotes a superuser from environment variables"

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL', '')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not password:
            self.stdout.write("ADMIN_USERNAME or ADMIN_PASSWORD not set, skipping.")
            return

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})

        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        if email:
            user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Existing user '{username}' promoted to superuser."))