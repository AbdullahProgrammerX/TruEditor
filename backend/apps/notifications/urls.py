"""
TruEditor - Notifications URLs
"""

from django.urls import path
from . import views

urlpatterns = [
    path('preferences/', views.EmailPreferenceView.as_view(), name='email-preferences'),
    path('email-log/', views.EmailLogListView.as_view(), name='email-log'),
]
