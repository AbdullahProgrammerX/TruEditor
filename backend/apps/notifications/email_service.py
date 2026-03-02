"""
TruEditor - Email Service
==========================
Centralized email sending with HTML templates and logging.

Developer: Abdullah Dogan
"""

import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import EmailLog, EmailPreference

logger = logging.getLogger(__name__)


def _send(email_type: str, recipient_email: str, subject: str,
          template_name: str, context: dict,
          recipient_user=None, submission=None) -> EmailLog:
    """
    Render an HTML template, send the email, and log the result.
    """
    log = EmailLog.objects.create(
        recipient=recipient_user,
        recipient_email=recipient_email,
        email_type=email_type,
        subject=subject,
        submission=submission,
        status=EmailLog.Status.PENDING,
    )

    try:
        context.setdefault('site_name', 'TruEditor')
        context.setdefault('site_url', settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else '')

        html_body = render_to_string(f'email/{template_name}.html', context)
        text_body = strip_tags(html_body)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=False)

        log.status = EmailLog.Status.SENT
        log.save(update_fields=['status'])
        logger.info("Email sent: [%s] %s → %s", email_type, subject, recipient_email)

    except Exception as exc:
        log.status = EmailLog.Status.FAILED
        log.error_message = str(exc)[:500]
        log.save(update_fields=['status', 'error_message'])
        logger.error("Email failed: [%s] %s → %s — %s", email_type, subject, recipient_email, exc)

    return log


# ── Public API ─────────────────────────────────────────────

def send_welcome_email(user) -> EmailLog | None:
    """Send welcome email after first ORCID login."""
    if not user.email:
        return None

    return _send(
        email_type=EmailLog.EmailType.WELCOME,
        recipient_email=user.email,
        subject='Welcome to TruEditor',
        template_name='welcome',
        context={
            'user_name': user.full_name or user.email,
            'orcid_id': user.orcid_id,
        },
        recipient_user=user,
    )


def send_submission_confirmation(submission) -> EmailLog | None:
    """Send confirmation after successful manuscript submission."""
    user = submission.created_by
    if not user or not user.email:
        return None

    prefs = EmailPreference.get_for_user(user)
    if not prefs.submission_confirmation:
        return None

    return _send(
        email_type=EmailLog.EmailType.SUBMISSION_CONFIRMATION,
        recipient_email=user.email,
        subject=f'Submission Confirmed — {submission.manuscript_id}',
        template_name='submission_confirmation',
        context={
            'user_name': user.full_name or user.email,
            'manuscript_id': submission.manuscript_id,
            'title': submission.title,
            'article_type': submission.get_article_type_display(),
            'author_count': submission.authors.count(),
            'file_count': submission.files.filter(is_active=True).count(),
        },
        recipient_user=user,
        submission=submission,
    )


def send_status_change(submission, old_status: str, new_status: str, notes: str = '') -> EmailLog | None:
    """Send notification when submission status changes."""
    from apps.submissions.models import Submission

    user = submission.created_by
    if not user or not user.email:
        return None

    prefs = EmailPreference.get_for_user(user)
    if not prefs.status_updates:
        return None

    status_labels = dict(Submission.Status.choices)

    return _send(
        email_type=EmailLog.EmailType.STATUS_CHANGE,
        recipient_email=user.email,
        subject=f'Status Update — {submission.manuscript_id}',
        template_name='status_change',
        context={
            'user_name': user.full_name or user.email,
            'manuscript_id': submission.manuscript_id,
            'title': submission.title,
            'old_status': status_labels.get(old_status, old_status),
            'new_status': status_labels.get(new_status, new_status),
            'notes': notes,
        },
        recipient_user=user,
        submission=submission,
    )


def send_withdrawal_confirmation(submission) -> EmailLog | None:
    """Send confirmation after manuscript withdrawal."""
    user = submission.created_by
    if not user or not user.email:
        return None

    return _send(
        email_type=EmailLog.EmailType.WITHDRAWAL_CONFIRMATION,
        recipient_email=user.email,
        subject=f'Withdrawal Confirmed — {submission.manuscript_id}',
        template_name='withdrawal_confirmation',
        context={
            'user_name': user.full_name or user.email,
            'manuscript_id': submission.manuscript_id,
            'title': submission.title,
        },
        recipient_user=user,
        submission=submission,
    )
