"""
TruEditor - User Views
======================
Views for user profile and authentication.

Developer: Abdullah Dogan
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.translation import gettext_lazy as _

from apps.common.response import success_response, error_response
from .serializers import (
    UserSerializer,
    UserProfileUpdateSerializer,
    ORCIDLoginSerializer,
    ORCIDCallbackSerializer,
    AuthResponseSerializer,
)


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
    
    Returns the URL to redirect user to ORCID for authentication.
    This will be fully implemented in the ORCID Authentication phase.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get ORCID authorization URL.
        
        Returns:
            authorization_url: URL to redirect to for ORCID login
        """
        # TODO: Implement in ORCID Authentication phase
        # This is a placeholder that returns an error until ORCID is configured
        return error_response(
            message=_('ORCID authentication is not yet configured'),
            code='ORCID_NOT_CONFIGURED',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class ORCIDCallbackView(APIView):
    """
    Handle ORCID OAuth callback.
    
    Exchanges authorization code for tokens and creates/updates user.
    This will be fully implemented in the ORCID Authentication phase.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle ORCID callback.
        
        Args:
            code: OAuth authorization code from ORCID
            state: Optional state parameter for CSRF protection
            
        Returns:
            access_token, refresh_token, user data
        """
        serializer = ORCIDCallbackSerializer(data=request.data)
        
        if not serializer.is_valid():
            return error_response(
                message=_('Invalid callback data'),
                code='VALIDATION_ERROR',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implement in ORCID Authentication phase
        return error_response(
            message=_('ORCID authentication is not yet configured'),
            code='ORCID_NOT_CONFIGURED',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class ORCIDSyncView(APIView):
    """
    Sync user profile from ORCID.
    
    Fetches latest data from ORCID API and updates user profile.
    This will be fully implemented in the ORCID Authentication phase.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Sync ORCID profile data.
        
        Returns:
            Updated user profile data
        """
        # TODO: Implement in ORCID Authentication phase
        return error_response(
            message=_('ORCID sync is not yet implemented'),
            code='ORCID_SYNC_NOT_IMPLEMENTED',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class LogoutView(APIView):
    """
    User logout endpoint.
    
    Invalidates refresh token and clears session.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Logout current user.
        
        Note: Client should also remove stored tokens.
        """
        # Refresh token blacklisting will be implemented with JWT
        # For now, just return success (client will clear tokens)
        return success_response(
            message=_('Logged out successfully')
        )
