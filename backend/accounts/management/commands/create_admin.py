"""
Management command to create a default admin superuser if one does not exist.
Used during Render deployment to ensure admin access.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a default admin superuser if none exists."

    def handle(self, *args, **options):
        email = os.getenv("ADMIN_EMAIL", "admin@jobboard.com")
        password = os.getenv("ADMIN_PASSWORD", "Admin@123")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Admin '{email}' already exists. Skipping."))
            return

        User.objects.create_superuser(
            email=email,
            password=password,
            first_name="Admin",
            last_name="User",
            role="admin",
        )
        self.stdout.write(self.style.SUCCESS(f"Admin superuser '{email}' created successfully."))
