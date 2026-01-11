"""
TruEditor - Common Views
========================
Health check and other common views.

Developer: Abdullah Dogan
"""

import os
from django.utils import timezone
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class HealthCheckView(APIView):
    """
    System health check endpoint.
    
    GET /api/v1/health/
    
    Response:
    {
        "success": true,
        "data": {
            "status": "healthy",
            "timestamp": "2026-01-10T12:00:00Z",
            "version": "1.0.0",
            "environment": "production",
            "checks": {
                "database": "ok",
                "cache": "ok"
            }
        }
    }
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Verify that the system is operational.
        Checks database and cache connections.
        """
        from django.conf import settings
        
        try:
            from core import __version__
        except ImportError:
            __version__ = '1.0.0'
        
        checks = {}
        overall_status = 'healthy'
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            checks['database'] = 'ok'
        except Exception as e:
            checks['database'] = f'error: {str(e)}'
            overall_status = 'unhealthy'
        
        # Redis/Cache check (optional)
        try:
            from django.core.cache import cache
            cache.set('health_check', 'ok', timeout=10)
            if cache.get('health_check') == 'ok':
                checks['cache'] = 'ok'
            else:
                checks['cache'] = 'error: cache read failed'
        except Exception as e:
            checks['cache'] = 'not_configured'  # Normal in development
        
        response_data = {
            'success': overall_status == 'healthy',
            'data': {
                'status': overall_status,
                'timestamp': timezone.now().isoformat(),
                'version': __version__,
                'service': 'TruEditor API',
                'environment': os.environ.get('ENV', 'development'),
                'checks': checks
            }
        }
        
        status_code = status.HTTP_200_OK if overall_status == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(response_data, status=status_code)


class ReadinessCheckView(APIView):
    """
    Kubernetes/Container readiness probe.
    Checks if the service is ready to accept traffic.
    
    GET /api/v1/health/ready/
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Check if the service is ready.
        """
        # Database connection is required
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            return Response(
                {'ready': False, 'reason': 'database_unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response({'ready': True}, status=status.HTTP_200_OK)


class LivenessCheckView(APIView):
    """
    Kubernetes/Container liveness probe.
    Checks if the service is alive.
    
    GET /api/v1/health/live/
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Verify that the service is alive.
        """
        return Response({'alive': True}, status=status.HTTP_200_OK)
