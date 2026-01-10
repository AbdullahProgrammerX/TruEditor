"""
TruEditor - Submissions URLs
============================
Makale gönderim endpoint'leri (Author Module).

Endpoint'ler:
- GET    /api/v1/submissions/              -> Gönderim listesi
- POST   /api/v1/submissions/              -> Yeni gönderim
- GET    /api/v1/submissions/{id}/         -> Gönderim detayı
- PUT    /api/v1/submissions/{id}/         -> Güncelleme
- PATCH  /api/v1/submissions/{id}/         -> Kısmi güncelleme
- DELETE /api/v1/submissions/{id}/         -> Silme
- POST   /api/v1/submissions/{id}/build_pdf/  -> PDF oluştur
- POST   /api/v1/submissions/{id}/approve/    -> Onayla
- POST   /api/v1/submissions/{id}/submit/     -> Gönder
- GET    /api/v1/submissions/{id}/task_status/ -> Görev durumu
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Views daha sonra oluşturulacak
# from .views import SubmissionViewSet

router = DefaultRouter()
# router.register('', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]
