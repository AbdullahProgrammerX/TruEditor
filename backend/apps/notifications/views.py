"""
TruEditor - Notification Views
"""

from rest_framework import generics, permissions
from rest_framework.views import APIView
from apps.common.response import success_response

from .models import EmailPreference, EmailLog
from .serializers import EmailPreferenceSerializer, EmailLogSerializer


class EmailPreferenceView(APIView):
    """
    GET  /notifications/preferences/   -> Get current email preferences
    PUT  /notifications/preferences/   -> Update email preferences
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        prefs = EmailPreference.get_for_user(request.user)
        serializer = EmailPreferenceSerializer(prefs)
        return success_response(data=serializer.data)

    def put(self, request):
        prefs = EmailPreference.get_for_user(request.user)
        serializer = EmailPreferenceSerializer(prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Email preferences updated')


class EmailLogListView(generics.ListAPIView):
    """
    GET /notifications/email-log/   -> List sent emails for the current user
    """
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmailLog.objects.filter(recipient=self.request.user).order_by('-created_at')[:50]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)
