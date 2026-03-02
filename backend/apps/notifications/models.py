"""
TruEditor - Notification Models
================================
Email log and user notification preferences.

Developer: Abdullah Dogan
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EmailLog(models.Model):
    """Tracks every email sent by the system."""

    class EmailType(models.TextChoices):
        WELCOME = 'welcome', _('Welcome')
        SUBMISSION_CONFIRMATION = 'submission_confirmation', _('Submission Confirmation')
        STATUS_CHANGE = 'status_change', _('Status Change')
        WITHDRAWAL_CONFIRMATION = 'withdrawal_confirmation', _('Withdrawal Confirmation')
        REVISION_REQUEST = 'revision_request', _('Revision Request')
        DECISION = 'decision', _('Decision Notification')
        OTHER = 'other', _('Other')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        FAILED = 'failed', _('Failed')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='email_logs',
    )
    recipient_email = models.EmailField()
    email_type = models.CharField(max_length=30, choices=EmailType.choices)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    error_message = models.TextField(blank=True)
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='email_logs',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Email Log')
        verbose_name_plural = _('Email Logs')

    def __str__(self):
        return f"[{self.get_email_type_display()}] {self.subject} → {self.recipient_email}"


class EmailPreference(models.Model):
    """Per-user email notification preferences."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_preferences',
    )
    submission_confirmation = models.BooleanField(default=True, help_text=_('Email when manuscript is submitted'))
    status_updates = models.BooleanField(default=True, help_text=_('Email when submission status changes'))
    revision_requests = models.BooleanField(default=True, help_text=_('Email when revision is requested'))
    decision_notifications = models.BooleanField(default=True, help_text=_('Email for editorial decisions'))
    system_announcements = models.BooleanField(default=True, help_text=_('General system announcements'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Email Preference')
        verbose_name_plural = _('Email Preferences')

    def __str__(self):
        return f"Email prefs for {self.user.email}"

    @classmethod
    def get_for_user(cls, user):
        """Get or create preferences for a user."""
        prefs, _ = cls.objects.get_or_create(user=user)
        return prefs
