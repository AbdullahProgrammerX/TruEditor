"""
TruEditor - Notification Serializers
"""

from rest_framework import serializers
from .models import EmailPreference, EmailLog


class EmailPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailPreference
        fields = [
            'submission_confirmation',
            'status_updates',
            'revision_requests',
            'decision_notifications',
            'system_announcements',
            'updated_at',
        ]
        read_only_fields = ['updated_at']


class EmailLogSerializer(serializers.ModelSerializer):
    email_type_display = serializers.CharField(source='get_email_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmailLog
        fields = [
            'id', 'email_type', 'email_type_display',
            'subject', 'recipient_email',
            'status', 'status_display',
            'created_at',
        ]
