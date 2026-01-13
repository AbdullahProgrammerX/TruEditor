"""
TruEditor - User Serializers
============================
Serializers for user profile and authentication.

Developer: Abdullah Dogan
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for read operations.
    Returns all public user information.
    """
    
    orcid_url = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            # Primary
            'id',
            
            # ORCID
            'orcid_id',
            'orcid_url',
            'last_orcid_sync',
            
            # Personal
            'email',
            'full_name',
            'given_name',
            'family_name',
            'display_name',
            
            # Contact
            'phone',
            'country',
            'city',
            'address',
            
            # Academic
            'title',
            'institution',
            'department',
            'expertise_areas',
            'bio',
            'website',
            
            # Roles
            'is_reviewer',
            'is_editor',
            'is_chief_editor',
            'reviewer_interests',
            
            # Status
            'is_active',
            'email_verified',
            'profile_completed',
            
            # Timestamps
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'id',
            'orcid_id',
            'orcid_url',
            'last_orcid_sync',
            'is_reviewer',
            'is_editor',
            'is_chief_editor',
            'is_active',
            'email_verified',
            'profile_completed',
            'date_joined',
            'last_login',
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Only allows editing of user-editable fields.
    """
    
    class Meta:
        model = User
        fields = [
            # Personal
            'email',
            'full_name',
            'given_name',
            'family_name',
            
            # Contact
            'phone',
            'country',
            'city',
            'address',
            
            # Academic
            'title',
            'institution',
            'department',
            'expertise_areas',
            'bio',
            'website',
            
            # Reviewer interests (if user is a reviewer)
            'reviewer_interests',
        ]
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if value:
            user = self.context.get('request').user
            if User.objects.exclude(pk=user.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    _('This email address is already in use.')
                )
        return value
    
    def validate_bio(self, value):
        """Validate bio length."""
        if value and len(value) > 1000:
            raise serializers.ValidationError(
                _('Biography cannot exceed 1000 characters.')
            )
        return value
    
    def validate_expertise_areas(self, value):
        """Validate expertise areas format."""
        if value:
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    _('Expertise areas must be a list.')
                )
            if len(value) > 10:
                raise serializers.ValidationError(
                    _('You can specify a maximum of 10 expertise areas.')
                )
        return value
    
    def update(self, instance, validated_data):
        """Update and check profile completion."""
        instance = super().update(instance, validated_data)
        instance.profile_completed = instance.check_profile_completion()
        instance.save(update_fields=['profile_completed', 'updated_at'])
        return instance


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal user serializer for nested relations.
    Used when user data is embedded in other objects.
    """
    
    orcid_url = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'orcid_id',
            'orcid_url',
            'full_name',
            'email',
            'institution',
        ]


class AuthResponseSerializer(serializers.Serializer):
    """
    Serializer for authentication response.
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserSerializer()


class ORCIDLoginSerializer(serializers.Serializer):
    """
    Serializer for ORCID login URL response.
    """
    authorization_url = serializers.URLField()


class ORCIDCallbackSerializer(serializers.Serializer):
    """
    Serializer for ORCID callback request.
    """
    code = serializers.CharField(
        required=True,
        help_text=_('OAuth authorization code from ORCID')
    )
    state = serializers.CharField(
        required=False,
        help_text=_('OAuth state parameter for CSRF protection')
    )
