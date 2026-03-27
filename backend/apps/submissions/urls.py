"""
TruEditor - Submissions URLs
============================
Makale gönderim endpoint'leri (Author Module).

Endpoint'ler:
- GET    /api/v1/submissions/                         -> Gönderim listesi
- POST   /api/v1/submissions/                         -> Yeni gönderim
- GET    /api/v1/submissions/{id}/                    -> Gönderim detayı
- PUT    /api/v1/submissions/{id}/                    -> Güncelleme
- PATCH  /api/v1/submissions/{id}/                    -> Kısmi güncelleme
- DELETE /api/v1/submissions/{id}/                    -> Silme
- POST   /api/v1/submissions/{id}/build_pdf/          -> PDF oluştur
- POST   /api/v1/submissions/{id}/approve/            -> Onayla
- POST   /api/v1/submissions/{id}/submit/             -> Gönder
- GET    /api/v1/submissions/{id}/task_status/         -> Görev durumu
- POST   /api/v1/submissions/{id}/notify-coauthors/   -> Ortak yazarları bilgilendir
- POST   /api/v1/submissions/verify/{token}/           -> Katkı doğrula (public)
- POST   /api/v1/submissions/verify/{token}/decline/   -> Katkı reddet (public)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet, verify_contribution, decline_contribution

router = DefaultRouter()
router.register('', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('verify/<uuid:token>/', verify_contribution, name='verify-contribution'),
    path('verify/<uuid:token>/decline/', decline_contribution, name='decline-contribution'),
    path('', include(router.urls)),
]
