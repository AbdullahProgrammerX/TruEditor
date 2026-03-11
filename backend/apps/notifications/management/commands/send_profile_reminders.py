"""
Send profile completion reminder emails to users who registered
more than 24 hours ago but haven't completed their profile yet.

Usage:
    python manage.py send_profile_reminders
"""

import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import User
from apps.notifications.email_service import send_profile_reminder

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send profile completion reminders to users with incomplete profiles (24h+ after registration)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='List users who would receive a reminder without actually sending',
        )

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=24)

        users = User.objects.filter(
            profile_completed=False,
            is_active=True,
            date_joined__lte=cutoff,
        ).exclude(email='').exclude(email__isnull=True)

        self.stdout.write(f"Found {users.count()} user(s) with incomplete profiles.")

        sent = 0
        for user in users:
            if options['dry_run']:
                self.stdout.write(f"  [DRY RUN] Would send to {user.email} ({user.orcid_id})")
                continue

            result = send_profile_reminder(user)
            if result:
                sent += 1
                self.stdout.write(f"  Sent reminder to {user.email}")
            else:
                self.stdout.write(f"  Skipped {user.email} (already sent or profile completed)")

        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"Dry run complete. {users.count()} user(s) eligible."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Done. Sent {sent} reminder(s)."))
