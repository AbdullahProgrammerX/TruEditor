"""
TruEditor - User Views
======================
Views for user profile and ORCID authentication.

OAuth Flow:
1. Frontend calls GET /api/v1/auth/orcid/login/ to get authorization URL
2. User is redirected to ORCID and logs in
3. ORCID redirects back to frontend with code
4. Frontend calls POST /api/v1/auth/orcid/callback/ with code
5. Backend exchanges code for tokens and creates/updates user
6. Backend returns JWT tokens to frontend

Developer: Abdullah Dogan
"""

import logging
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from apps.common.response import success_response, error_response
from .models import User
from .serializers import (
    UserSerializer,
    UserProfileUpdateSerializer,
    ORCIDCallbackSerializer,
)
from .orcid_service import ORCIDService, ORCIDAuthError

logger = logging.getLogger(__name__)


class ProfileView(APIView):
    """
    User profile endpoint.
    
    GET: Returns the authenticated user's profile
    PUT: Updates the authenticated user's profile
    PATCH: Partially updates the authenticated user's profile
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get current user's profile.
        
        Returns:
            User profile data
        """
        serializer = UserSerializer(request.user)
        return success_response(
            data=serializer.data,
            message=_('Profile retrieved successfully')
        )
    
    def put(self, request):
        """
        Update current user's profile (full update).
        
        Returns:
            Updated user profile data
        """
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            # Return full user data
            user_serializer = UserSerializer(request.user)
            return success_response(
                data=user_serializer.data,
                message=_('Profile updated successfully')
            )
        
        return error_response(
            message=_('Validation error'),
            code='VALIDATION_ERROR',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request):
        """
        Partially update current user's profile.
        
        Returns:
            Updated user profile data
        """
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            # Return full user data
            user_serializer = UserSerializer(request.user)
            return success_response(
                data=user_serializer.data,
                message=_('Profile updated successfully')
            )
        
        return error_response(
            message=_('Validation error'),
            code='VALIDATION_ERROR',
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ORCIDLoginView(APIView):
    """
    Get ORCID OAuth authorization URL.
    
    GET /api/v1/auth/orcid/login/
    
    Returns the URL to redirect user to ORCID for authentication.
    The state parameter should be stored by the frontend and verified
    in the callback for CSRF protection.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get ORCID authorization URL.
        
        Query Parameters:
            redirect_uri: Optional custom redirect URI (must be whitelisted)
        
        Returns:
            {
                "success": true,
                "data": {
                    "authorization_url": "https://orcid.org/oauth/authorize?...",
                    "state": "random-state-token"
                }
            }
        """
        # Check if ORCID is configured
        if not settings.ORCID_CLIENT_ID or not settings.ORCID_CLIENT_SECRET:
            logger.error("ORCID credentials not configured")
            return error_response(
                message=_('ORCID authentication is not configured. Please contact the administrator.'),
                code='ORCID_NOT_CONFIGURED',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            service = ORCIDService()
            authorization_url, state = service.get_authorization_url()
            
            logger.info(f"Generated ORCID authorization URL with state: {state[:8]}...")
            
            return success_response(
                data={
                    'authorization_url': authorization_url,
                    'state': state,
                },
                message=_('Authorization URL generated successfully')
            )
            
        except Exception as e:
            logger.exception("Failed to generate ORCID authorization URL")
            return error_response(
                message=_('Failed to generate authorization URL'),
                code='ORCID_ERROR',
                details={'error': str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ORCIDCallbackView(APIView):
    """
    Handle ORCID OAuth callback.
    
    POST /api/v1/auth/orcid/callback/
    
    Exchanges authorization code for tokens and creates/updates user.
    Returns JWT access and refresh tokens for the application.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle ORCID callback.
        
        Request Body:
            {
                "code": "authorization-code-from-orcid",
                "state": "state-from-authorization-url"  // optional, for CSRF verification
            }
            
        Returns:
            {
                "success": true,
                "data": {
                    "access_token": "jwt-access-token",
                    "refresh_token": "jwt-refresh-token",
                    "user": { ... user profile ... },
                    "is_new_user": true/false
                }
            }
        """
        serializer = ORCIDCallbackSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message=_('Invalid callback data'),
                code='VALIDATION_ERROR',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        code = serializer.validated_data['code']
        
        # Check if ORCID is configured
        if not settings.ORCID_CLIENT_ID or not settings.ORCID_CLIENT_SECRET:
            logger.error("ORCID credentials not configured")
            return error_response(
                message=_('ORCID authentication is not configured'),
                code='ORCID_NOT_CONFIGURED',
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            service = ORCIDService()
            
            # Step 1: Exchange code for token
            logger.info("Exchanging ORCID authorization code for token")
            token_response = service.exchange_code(code)
            logger.info(f"Received ORCID token for user: {token_response.orcid_id}")
            
            # Step 2: Fetch profile from ORCID API
            logger.info(f"Fetching profile for ORCID: {token_response.orcid_id}")
            profile = service.get_profile(
                token_response.orcid_id, 
                token_response.access_token
            )
            
            # Step 3: Create or update user
            user, is_new_user = service.get_or_create_user(token_response, profile)
            logger.info(f"User {'created' if is_new_user else 'updated'}: {user.orcid_id}")
            
            # Step 4: Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Step 5: Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Step 6: Serialize user data
            user_serializer = UserSerializer(user)
            
            return success_response(
                data={
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user_serializer.data,
                    'is_new_user': is_new_user,
                },
                message=_('Login successful') if not is_new_user else _('Account created successfully')
            )
            
        except ORCIDAuthError as e:
            logger.warning(f"ORCID authentication failed: {str(e)}")
            return error_response(
                message=str(e),
                code='ORCID_AUTH_ERROR',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        except Exception as e:
            logger.exception("Unexpected error during ORCID callback")
            return error_response(
                message=_('An unexpected error occurred during authentication'),
                code='AUTHENTICATION_ERROR',
                details={'error': str(e)} if settings.DEBUG else None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ORCIDSyncView(APIView):
    """
    Sync user profile from ORCID.
    
    POST /api/v1/auth/orcid/sync/
    
    Fetches latest data from ORCID API and updates user profile.
    Requires authentication.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Sync ORCID profile data.
        
        Returns:
            Updated user profile data
        """
        user = request.user
        
        if not user.orcid_access_token:
            return error_response(
                message=_('No ORCID connection found. Please log in with ORCID first.'),
                code='NO_ORCID_TOKEN',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = ORCIDService()
            updated_user = service.sync_user_profile(user)
            
            user_serializer = UserSerializer(updated_user)
            
            logger.info(f"Profile synced from ORCID for user: {user.orcid_id}")
            
            return success_response(
                data=user_serializer.data,
                message=_('Profile synced successfully from ORCID')
            )
            
        except ORCIDAuthError as e:
            logger.warning(f"ORCID sync failed for user {user.orcid_id}: {str(e)}")
            return error_response(
                message=str(e),
                code='ORCID_SYNC_ERROR',
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error during ORCID sync for user {user.orcid_id}")
            return error_response(
                message=_('Failed to sync profile from ORCID'),
                code='SYNC_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """
    User logout endpoint.
    
    POST /api/v1/auth/logout/
    
    Blacklists the refresh token to invalidate the session.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Logout current user.
        
        Request Body (optional):
            {
                "refresh_token": "jwt-refresh-token"  // Token to blacklist
            }
        
        Note: Client should also remove stored tokens from local storage.
        """
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f"User {request.user.orcid_id} logged out - token blacklisted")
            except Exception as e:
                # Token might be invalid or already blacklisted
                logger.warning(f"Failed to blacklist token for user {request.user.orcid_id}: {str(e)}")
        
        return success_response(
            message=_('Logged out successfully')
        )
