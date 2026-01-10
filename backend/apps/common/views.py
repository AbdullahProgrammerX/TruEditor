"""
TruEditor - Common Views
========================
Health check ve diğer ortak view'lar.
"""

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


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
            "version": "1.0.0"
        }
    }
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def get(self, request):
        """
        Sistemin çalışır durumda olduğunu doğrular.
        """
        from core import __version__
        
        return Response({
            'success': True,
            'data': {
                'status': 'healthy',
                'timestamp': timezone.now().isoformat(),
                'version': __version__,
                'service': 'TruEditor API'
            }
        })
