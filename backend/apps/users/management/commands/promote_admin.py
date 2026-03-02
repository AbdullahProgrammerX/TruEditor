"""
One-time command to promote an ORCID user to superuser with a password.
Safe to run multiple times — only acts if the user isn't already staff.
"""
import os
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Promote an ORCID user to Django admin superuser'

    def handle(self, *args, **options):
        orcid_id = os.environ.get('ADMIN_ORCID_ID', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '').strip()

        if not orcid_id or not password:
            self.stdout.write(self.style.WARNING(
                'ADMIN_ORCID_ID or ADMIN_PASSWORD not set — skipping.'
            ))
            return

        try:
            user = User.objects.get(orcid_id=orcid_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                f'User with ORCID {orcid_id} not found.'
            ))
            return

        if user.is_superuser and user.is_staff:
            self.stdout.write(self.style.SUCCESS(
                f'{user.email} is already a superuser.'
            ))
            return

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=['password', 'is_staff', 'is_superuser'])

        self.stdout.write(self.style.SUCCESS(
            f'Promoted {user.email} (ORCID: {orcid_id}) to superuser.'
        ))
