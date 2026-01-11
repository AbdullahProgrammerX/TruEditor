"""
TruEditor - Common Views
========================
Health check ve diğer ortak view'lar.

Geliştirici: Abdullah Doğan
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
    Sistem sağlık kontrolü endpoint'i.
    
    GET /api/v1/health/
    
    Dönen yanıt:
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
        Sistemin çalışır durumda olduğunu doğrular.
        Database ve cache bağlantılarını kontrol eder.
        """
        from django.conf import settings
        
        try:
            from core import __version__
        except ImportError:
            __version__ = '1.0.0'
        
        checks = {}
        overall_status = 'healthy'
        
        # Database kontrolü
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            checks['database'] = 'ok'
        except Exception as e:
            checks['database'] = f'error: {str(e)}'
            overall_status = 'unhealthy'
        
        # Redis/Cache kontrolü (opsiyonel)
        try:
            from django.core.cache import cache
            cache.set('health_check', 'ok', timeout=10)
            if cache.get('health_check') == 'ok':
                checks['cache'] = 'ok'
            else:
                checks['cache'] = 'error: cache read failed'
        except Exception as e:
            checks['cache'] = 'not_configured'  # Development'ta normal
        
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
    Servisin trafik almaya hazır olup olmadığını kontrol eder.
    
    GET /api/v1/ready/
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Servisin hazır olup olmadığını kontrol eder.
        """
        # Database bağlantısı zorunlu
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
    Servisin canlı olup olmadığını kontrol eder.
    
    GET /api/v1/live/
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Servisin canlı olduğunu doğrular.
        """
        return Response({'alive': True}, status=status.HTTP_200_OK)
