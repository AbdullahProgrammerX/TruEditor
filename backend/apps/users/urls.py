"""
TruEditor - Users URLs
======================
ORCID authentication and user profile endpoints.

Endpoints:
- GET  /api/v1/auth/orcid/login/     -> Get ORCID login URL
- POST /api/v1/auth/orcid/callback/  -> OAuth callback
- POST /api/v1/auth/orcid/sync/      -> Sync ORCID profile
- POST /api/v1/auth/logout/          -> Logout
- POST /api/v1/auth/token/refresh/   -> Refresh token
- GET  /api/v1/auth/profile/         -> Get profile
- PUT  /api/v1/auth/profile/         -> Update profile (full)
- PATCH /api/v1/auth/profile/        -> Update profile (partial)

Developer: Abdullah Dogan
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ProfileView,
    ORCIDLoginView,
    ORCIDCallbackView,
    ORCIDSyncView,
    LogoutView,
)

app_name = 'users'

urlpatterns = [
    # ORCID Authentication
    path('orcid/login/', ORCIDLoginView.as_view(), name='orcid-login'),
    path('orcid/callback/', ORCIDCallbackView.as_view(), name='orcid-callback'),
    path('orcid/sync/', ORCIDSyncView.as_view(), name='orcid-sync'),
    
    # JWT Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
]
