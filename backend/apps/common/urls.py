"""
TruEditor - Common URLs
=======================
Health check ve diğer ortak endpoint'ler.

Geliştirici: Abdullah Doğan
"""

from django.urls import path
from .views import HealthCheckView, ReadinessCheckView, LivenessCheckView

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
    path('ready/', ReadinessCheckView.as_view(), name='readiness-check'),
    path('live/', LivenessCheckView.as_view(), name='liveness-check'),
]
