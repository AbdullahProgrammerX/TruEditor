"""
TruEditor - Users URLs
======================
ORCID kimlik doğrulama ve kullanıcı profili endpoint'leri.

Endpoint'ler:
- GET  /api/v1/auth/orcid/login/     -> ORCID login URL'i
- POST /api/v1/auth/orcid/callback/  -> OAuth callback
- POST /api/v1/auth/logout/          -> Çıkış yap
- POST /api/v1/auth/token/refresh/   -> Token yenile
- GET  /api/v1/auth/profile/         -> Profil bilgileri
- PUT  /api/v1/auth/profile/         -> Profil güncelle
- POST /api/v1/auth/orcid/sync/      -> ORCID senkronize
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# Views daha sonra oluşturulacak
# from .views import (
#     ORCIDLoginView,
#     ORCIDCallbackView,
#     LogoutView,
#     ProfileView,
#     ORCIDSyncView,
# )

urlpatterns = [
    # ORCID Authentication
    # path('orcid/login/', ORCIDLoginView.as_view(), name='orcid-login'),
    # path('orcid/callback/', ORCIDCallbackView.as_view(), name='orcid-callback'),
    # path('orcid/sync/', ORCIDSyncView.as_view(), name='orcid-sync'),
    
    # JWT Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Logout
    # path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile
    # path('profile/', ProfileView.as_view(), name='profile'),
]
