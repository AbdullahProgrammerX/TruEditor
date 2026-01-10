"""
TruEditor - Files URLs
======================
Dosya yükleme ve yönetim endpoint'leri.

Endpoint'ler:
- POST   /api/v1/files/                -> Dosya yükle
- DELETE /api/v1/files/{id}/           -> Dosya sil
- GET    /api/v1/files/{id}/download/  -> Presigned URL al
- POST   /api/v1/files/reorder/        -> Sıralama güncelle
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Views daha sonra oluşturulacak
# from .views import ManuscriptFileViewSet

router = DefaultRouter()
# router.register('', ManuscriptFileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
