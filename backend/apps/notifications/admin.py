from django.contrib import admin
from .models import EmailLog, EmailPreference


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['email_type', 'subject', 'recipient_email', 'status', 'created_at']
    list_filter = ['email_type', 'status', 'created_at']
    search_fields = ['recipient_email', 'subject']
    readonly_fields = ['id', 'recipient', 'recipient_email', 'email_type', 'subject', 'status', 'error_message', 'submission', 'created_at']


@admin.register(EmailPreference)
class EmailPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'submission_confirmation', 'status_updates', 'revision_requests', 'decision_notifications']
    list_filter = ['submission_confirmation', 'status_updates']
