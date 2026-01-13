"""
TruEditor - ORCID OAuth Service
===============================
Handles ORCID OAuth 2.0 authentication flow.

OAuth Flow:
1. Generate authorization URL -> redirect user to ORCID
2. User logs in at ORCID and grants permission
3. ORCID redirects back with authorization code
4. Exchange code for access token
5. Fetch user profile from ORCID API
6. Create/update user in database

Developer: Abdullah Dogan
"""

import secrets
import requests
from urllib.parse import urlencode
from typing import Optional, Tuple
from dataclasses import dataclass
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import User


@dataclass
class ORCIDConfig:
    """ORCID OAuth configuration."""
    client_id: str
    client_secret: str
    redirect_uri: str
    base_url: str  # https://orcid.org or https://sandbox.orcid.org
    api_url: str   # https://api.orcid.org or https://api.sandbox.orcid.org
    
    @classmethod
    def from_settings(cls) -> 'ORCIDConfig':
        """Create config from Django settings."""
        return cls(
            client_id=settings.ORCID_CLIENT_ID,
            client_secret=settings.ORCID_CLIENT_SECRET,
            redirect_uri=settings.ORCID_REDIRECT_URI,
            base_url=settings.ORCID_BASE_URL,
            api_url=settings.ORCID_API_URL,
        )


@dataclass
class ORCIDTokenResponse:
    """Response from ORCID token endpoint."""
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: str
    orcid_id: str
    name: Optional[str] = None


@dataclass
class ORCIDProfile:
    """ORCID profile data."""
    orcid_id: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    institution: Optional[str] = None
    department: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    raw_data: Optional[dict] = None


class ORCIDService:
    """
    Service for handling ORCID OAuth 2.0 authentication.
    
    Usage:
        service = ORCIDService()
        
        # Step 1: Get authorization URL
        auth_url, state = service.get_authorization_url()
        
        # Step 2: After callback, exchange code for token
        token_response = service.exchange_code(code)
        
        # Step 3: Fetch profile
        profile = service.get_profile(token_response.orcid_id, token_response.access_token)
        
        # Step 4: Create or update user
        user, created = service.get_or_create_user(token_response, profile)
    """
    
    def __init__(self, config: Optional[ORCIDConfig] = None):
        """Initialize with optional custom config."""
        self.config = config or ORCIDConfig.from_settings()
    
    def get_authorization_url(self, state: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate ORCID authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection.
                   If not provided, a random state will be generated.
        
        Returns:
            Tuple of (authorization_url, state)
        """
        if state is None:
            state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.config.client_id,
            'response_type': 'code',
            'scope': '/authenticate',  # Public API only supports /authenticate
            'redirect_uri': self.config.redirect_uri,
            'state': state,
        }
        
        auth_url = f"{self.config.base_url}/oauth/authorize?{urlencode(params)}"
        return auth_url, state
    
    def exchange_code(self, code: str) -> ORCIDTokenResponse:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from ORCID callback
            
        Returns:
            ORCIDTokenResponse with access token and user info
            
        Raises:
            ORCIDAuthError: If token exchange fails
        """
        token_url = f"{self.config.base_url}/oauth/token"
        
        data = {
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config.redirect_uri,
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(token_url, data=data, headers=headers, timeout=30)
        
        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('error_description', 'Token exchange failed')
            raise ORCIDAuthError(f"ORCID token exchange failed: {error_msg}")
        
        token_data = response.json()
        
        return ORCIDTokenResponse(
            access_token=token_data['access_token'],
            token_type=token_data.get('token_type', 'Bearer'),
            refresh_token=token_data.get('refresh_token', ''),
            expires_in=token_data.get('expires_in', 631138518),  # ~20 years default
            scope=token_data.get('scope', ''),
            orcid_id=token_data['orcid'],
            name=token_data.get('name'),
        )
    
    def refresh_access_token(self, refresh_token: str) -> ORCIDTokenResponse:
        """
        Refresh an expired access token.
        
        Args:
            refresh_token: Refresh token from previous authentication
            
        Returns:
            New ORCIDTokenResponse with fresh access token
        """
        token_url = f"{self.config.base_url}/oauth/token"
        
        data = {
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        response = requests.post(token_url, data=data, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise ORCIDAuthError("Failed to refresh ORCID token")
        
        token_data = response.json()
        
        return ORCIDTokenResponse(
            access_token=token_data['access_token'],
            token_type=token_data.get('token_type', 'Bearer'),
            refresh_token=token_data.get('refresh_token', refresh_token),
            expires_in=token_data.get('expires_in', 631138518),
            scope=token_data.get('scope', ''),
            orcid_id=token_data['orcid'],
            name=token_data.get('name'),
        )
    
    def get_profile(self, orcid_id: str, access_token: str) -> ORCIDProfile:
        """
        Fetch user profile from ORCID API.
        
        Note: With Public API (/authenticate scope only), we can only get
        limited public information. Full profile data requires Member API
        with /read-limited scope.
        
        Args:
            orcid_id: User's ORCID iD
            access_token: Valid access token
            
        Returns:
            ORCIDProfile with user data
        """
        # Try to fetch public record (works with Public API)
        profile_url = f"{self.config.api_url}/v3.0/{orcid_id}/person"
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        
        try:
            response = requests.get(profile_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_person_data(orcid_id, data)
            else:
                # Public API might not allow this, return minimal profile
                return ORCIDProfile(orcid_id=orcid_id)
                
        except Exception:
            # Return minimal profile if API call fails
            return ORCIDProfile(orcid_id=orcid_id)
    
    def _parse_person_data(self, orcid_id: str, data: dict) -> ORCIDProfile:
        """Parse ORCID person endpoint response."""
        # Name
        name_data = data.get('name', {})
        given_name = None
        family_name = None
        
        if name_data:
            given_names = name_data.get('given-names', {})
            if given_names:
                given_name = given_names.get('value')
            
            family_names = name_data.get('family-name', {})
            if family_names:
                family_name = family_names.get('value')
        
        # Email (if public)
        email = None
        emails_data = data.get('emails', {}).get('email', [])
        for email_entry in emails_data:
            if email_entry.get('verified'):
                email = email_entry.get('email')
                break
        if not email and emails_data:
            email = emails_data[0].get('email')
        
        # Country (if public)
        country = None
        addresses = data.get('addresses', {}).get('address', [])
        if addresses:
            country_data = addresses[0].get('country', {})
            country = country_data.get('value') if country_data else None
        
        # Biography (if public)
        bio = None
        biography = data.get('biography', {})
        if biography:
            bio = biography.get('content', '')[:1000]
        
        # Website (if public)
        website = None
        researcher_urls = data.get('researcher-urls', {}).get('researcher-url', [])
        if researcher_urls:
            url_data = researcher_urls[0].get('url', {})
            website = url_data.get('value') if url_data else None
        
        return ORCIDProfile(
            orcid_id=orcid_id,
            given_name=given_name,
            family_name=family_name,
            email=email,
            country=country,
            bio=bio,
            website=website,
            raw_data=data,
        )
    
    def get_or_create_user(
        self, 
        token_response: ORCIDTokenResponse, 
        profile: ORCIDProfile
    ) -> Tuple[User, bool]:
        """
        Get existing user or create new one from ORCID data.
        
        Args:
            token_response: Token data from ORCID
            profile: Profile data from ORCID API
            
        Returns:
            Tuple of (user, created) where created is True if new user
        """
        # Try to find existing user
        try:
            user = User.objects.get(orcid_id=token_response.orcid_id)
            created = False
        except User.DoesNotExist:
            user = User(orcid_id=token_response.orcid_id)
            user.set_unusable_password()  # ORCID users don't have passwords
            created = True
        
        # Update tokens
        user.orcid_access_token = token_response.access_token
        user.orcid_refresh_token = token_response.refresh_token
        user.orcid_token_expires = timezone.now() + timedelta(seconds=token_response.expires_in)
        
        # Update profile from ORCID (only if not already set or if new user)
        if created or not user.full_name:
            if profile.given_name:
                user.given_name = profile.given_name
            if profile.family_name:
                user.family_name = profile.family_name
            
            full_name = f"{profile.given_name or ''} {profile.family_name or ''}".strip()
            if full_name:
                user.full_name = full_name
            elif token_response.name:
                user.full_name = token_response.name
        
        if created or not user.email:
            if profile.email:
                user.email = profile.email
        
        if created or not user.country:
            if profile.country:
                user.country = profile.country
        
        if created or not user.institution:
            if profile.institution:
                user.institution = profile.institution
        
        if created or not user.department:
            if profile.department:
                user.department = profile.department
        
        if created or not user.bio:
            if profile.bio:
                user.bio = profile.bio
        
        if created or not user.website:
            if profile.website:
                user.website = profile.website
        
        # Store raw ORCID data
        user.orcid_data = profile.raw_data or {}
        
        user.last_orcid_sync = timezone.now()
        user.last_login = timezone.now()
        
        # Check profile completion
        user.profile_completed = user.check_profile_completion()
        
        user.save()
        
        return user, created
    
    def sync_user_profile(self, user: User) -> User:
        """
        Sync user profile from ORCID API.
        
        Args:
            user: User to sync
            
        Returns:
            Updated user
        """
        if not user.orcid_access_token:
            raise ORCIDAuthError("User has no ORCID access token")
        
        # Check if token needs refresh
        if user.orcid_token_expires and user.orcid_token_expires < timezone.now():
            if user.orcid_refresh_token:
                token_response = self.refresh_access_token(user.orcid_refresh_token)
                user.orcid_access_token = token_response.access_token
                user.orcid_refresh_token = token_response.refresh_token
                user.orcid_token_expires = timezone.now() + timedelta(seconds=token_response.expires_in)
            else:
                raise ORCIDAuthError("ORCID token expired and no refresh token available")
        
        # Fetch profile
        profile = self.get_profile(user.orcid_id, user.orcid_access_token)
        
        # Update user data
        if profile.raw_data:
            user.update_from_orcid(profile.raw_data)
        
        return user


class ORCIDAuthError(Exception):
    """Exception raised for ORCID authentication errors."""
    pass
