"""
TruEditor - Submission Serializers
===================================
Serializers for manuscript submissions and authors.

Developer: Abdullah Dogan
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Submission, Author
from apps.users.serializers import UserMinimalSerializer
from apps.files.serializers import ManuscriptFileSerializer


class AuthorshipSerializer(serializers.ModelSerializer):
    """
    Author serializer for submission authors.
    """
    
    full_name = serializers.ReadOnlyField()
    affiliation = serializers.ReadOnlyField()
    user = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'id',
            'user',
            'orcid_id',
            'given_name',
            'family_name',
            'full_name',
            'email',
            'institution',
            'department',
            'country',
            'city',
            'affiliation',
            'order',
            'is_corresponding',
            'contribution',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SubmissionListSerializer(serializers.ModelSerializer):
    """
    Submission list serializer for dashboard.
    Returns summary information for listing.
    """
    
    submitter = UserMinimalSerializer(read_only=True)
    author_count = serializers.ReadOnlyField()
    file_count = serializers.ReadOnlyField()
    corresponding_author = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id',
            'manuscript_id',
            'title',
            'article_type',
            'status',
            'status_display',
            'submitter',
            'author_count',
            'file_count',
            'corresponding_author',
            'created_at',
            'updated_at',
            'submitted_at',
        ]
        read_only_fields = [
            'id',
            'manuscript_id',
            'status',
            'status_display',
            'created_at',
            'updated_at',
            'submitted_at',
        ]
    
    def get_corresponding_author(self, obj):
        """Return corresponding author information."""
        author = obj.get_corresponding_author()
        if author:
            return {
                'name': author.full_name,
                'email': author.email,
                'orcid_id': author.orcid_id,
            }
        return None


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """
    Full submission detail serializer.
    Includes all fields and related objects.
    """
    
    submitter = UserMinimalSerializer(read_only=True)
    authors = AuthorshipSerializer(many=True, read_only=True)
    files = ManuscriptFileSerializer(many=True, read_only=True)
    assigned_editor = UserMinimalSerializer(read_only=True)
    author_count = serializers.ReadOnlyField()
    file_count = serializers.ReadOnlyField()
    is_editable = serializers.ReadOnlyField()
    can_be_withdrawn = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    article_type_display = serializers.CharField(source='get_article_type_display', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            # Primary
            'id',
            'manuscript_id',
            
            # Status
            'status',
            'status_display',
            'is_editable',
            'can_be_withdrawn',
            
            # Submission Info
            'submitter',
            'article_type',
            'article_type_display',
            'language',
            
            # Manuscript Info
            'title',
            'title_en',
            'abstract',
            'abstract_en',
            'keywords',
            'keywords_en',
            
            # Cover Letter & Ethics
            'cover_letter',
            'ethics_statement',
            'ethics_approval_number',
            'conflict_of_interest',
            'funding_statement',
            
            # Wizard Progress
            'wizard_step',
            'wizard_data',
            
            # Revision Info
            'revision_number',
            'revision_notes',
            'revision_deadline',
            
            # Editor Assignment
            'assigned_editor',
            'editor_notes',
            'editor_decision',
            'editor_decision_date',
            
            # Relations
            'authors',
            'files',
            'author_count',
            'file_count',
            
            # Timestamps
            'created_at',
            'updated_at',
            'submitted_at',
            'accepted_at',
            'published_at',
        ]
        read_only_fields = [
            'id',
            'manuscript_id',
            'status',
            'status_display',
            'is_editable',
            'can_be_withdrawn',
            'article_type_display',
            'submitter',
            'assigned_editor',
            'revision_number',
            'editor_decision',
            'editor_decision_date',
            'created_at',
            'updated_at',
            'submitted_at',
            'accepted_at',
            'published_at',
        ]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new submission.
    Creates a DRAFT submission.
    """
    
    class Meta:
        model = Submission
        fields = [
            'title',
            'title_en',
            'abstract',
            'abstract_en',
            'keywords',
            'keywords_en',
            'article_type',
            'language',
            'cover_letter',
            'ethics_statement',
            'ethics_approval_number',
            'conflict_of_interest',
            'funding_statement',
            'wizard_step',
            'wizard_data',
        ]
    
    def validate_keywords(self, value):
        """Validate keywords format."""
        if value:
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    _('Keywords must be a list.')
                )
            if len(value) > 10:
                raise serializers.ValidationError(
                    _('Maximum 10 keywords allowed.')
                )
        return value
    
    def validate_keywords_en(self, value):
        """Validate English keywords format."""
        if value:
            if not isinstance(value, list):
                raise serializers.ValidationError(
                    _('English keywords must be a list.')
                )
            if len(value) > 10:
                raise serializers.ValidationError(
                    _('Maximum 10 English keywords allowed.')
                )
        return value
    
    def validate_abstract(self, value):
        """Validate abstract length."""
        if value and len(value) > 5000:
            raise serializers.ValidationError(
                _('Abstract cannot exceed 5000 characters.')
            )
        return value
    
    def validate_wizard_step(self, value):
        """Validate wizard step range."""
        if value < 1 or value > 6:
            raise serializers.ValidationError(
                _('Wizard step must be between 1 and 6.')
            )
        return value
    
    def create(self, validated_data):
        """Create a new submission as DRAFT."""
        validated_data['submitter'] = self.context['request'].user
        validated_data['status'] = Submission.Status.DRAFT
        return super().create(validated_data)


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a submission.
    Only allows updates when status is DRAFT or REVISION_REQUIRED.
    """
    
    class Meta:
        model = Submission
        fields = [
            'title',
            'title_en',
            'abstract',
            'abstract_en',
            'keywords',
            'keywords_en',
            'article_type',
            'language',
            'cover_letter',
            'ethics_statement',
            'ethics_approval_number',
            'conflict_of_interest',
            'funding_statement',
            'wizard_step',
            'wizard_data',
        ]
    
    def validate(self, attrs):
        """Validate that submission can be edited."""
        instance = self.instance
        
        if not instance.is_editable:
            raise serializers.ValidationError(
                _('This submission cannot be edited in its current status.')
            )
        
        return attrs
    
    def validate_keywords(self, value):
        """Validate keywords format."""
        if value and len(value) > 10:
            raise serializers.ValidationError(
                _('Maximum 10 keywords allowed.')
            )
        return value
    
    def validate_abstract(self, value):
        """Validate abstract length."""
        if value and len(value) > 5000:
            raise serializers.ValidationError(
                _('Abstract cannot exceed 5000 characters.')
            )
        return value


class AuthorCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating authors.
    """
    
    submission = serializers.PrimaryKeyRelatedField(
        queryset=Submission.objects.all(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Author
        fields = [
            'submission',
            'user',
            'orcid_id',
            'given_name',
            'family_name',
            'email',
            'institution',
            'department',
            'country',
            'city',
            'order',
            'is_corresponding',
            'contribution',
        ]
    
    def validate_email(self, value):
        """Validate email format."""
        if not value:
            raise serializers.ValidationError(
                _('Email is required.')
            )
        return value
    
    def validate(self, attrs):
        """Validate author data."""
        # If user is provided, sync ORCID ID
        if attrs.get('user') and not attrs.get('orcid_id'):
            attrs['orcid_id'] = attrs['user'].orcid_id
        
        # Ensure at least name is provided
        if not attrs.get('given_name') and not attrs.get('family_name'):
            raise serializers.ValidationError(
                _('At least given name or family name must be provided.')
            )
        
        return attrs
    
    def create(self, validated_data):
        """Create author and ensure only one corresponding author."""
        author = super().create(validated_data)
        
        # If this is corresponding, unset others
        if author.is_corresponding:
            Author.objects.filter(
                submission=author.submission,
                is_corresponding=True
            ).exclude(pk=author.pk).update(is_corresponding=False)
        
        return author


class SubmissionSubmitSerializer(serializers.Serializer):
    """
    Serializer for submission approval and final submission.
    """
    
    confirm = serializers.BooleanField(
        required=True,
        help_text=_('Confirmation that all information is correct')
    )
    
    def validate_confirm(self, value):
        """Validate confirmation."""
        if not value:
            raise serializers.ValidationError(
                _('You must confirm to submit.')
            )
        return value
