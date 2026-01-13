"""
TruEditor - File Serializers
=============================
Serializers for file upload and management.

Developer: Abdullah Dogan
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from .models import ManuscriptFile
from apps.submissions.models import Submission


class ManuscriptFileSerializer(serializers.ModelSerializer):
    """
    Serializer for manuscript files.
    """
    
    file_size_human = serializers.ReadOnlyField()
    file_extension = serializers.ReadOnlyField()
    is_image = serializers.ReadOnlyField()
    is_document = serializers.ReadOnlyField()
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ManuscriptFile
        fields = [
            'id',
            'submission',
            'file',
            'file_type',
            'file_type_display',
            'original_filename',
            'file_size',
            'file_size_human',
            'file_extension',
            'mime_type',
            'description',
            'caption',
            'order',
            'revision_number',
            'is_active',
            'is_primary',
            'is_image',
            'is_document',
            'download_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'file_size',
            'file_size_human',
            'file_extension',
            'mime_type',
            'is_image',
            'is_document',
            'created_at',
            'updated_at',
        ]
    
    def get_download_url(self, obj):
        """Generate presigned download URL."""
        if obj.file:
            return obj.get_download_url(expiration=900)  # 15 minutes
        return None


class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for file upload.
    Handles multipart form data.
    """
    
    file = serializers.FileField(
        required=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'xlsx', 'xls']
            )
        ],
        help_text=_('Allowed formats: DOC, DOCX, PDF, JPG, PNG, TIFF, XLS, XLSX')
    )
    
    class Meta:
        model = ManuscriptFile
        fields = [
            'file',
            'file_type',
            'description',
            'caption',
            'order',
        ]
    
    def validate_file(self, value):
        """Validate file size and type."""
        # Max file size: 50MB
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        if value.size > max_size:
            raise serializers.ValidationError(
                _('File size cannot exceed 50MB.')
            )
        
        return value
    
    def validate(self, attrs):
        """Validate submission status."""
        submission = self.context.get('submission')
        
        if not submission:
            raise serializers.ValidationError(
                _('Submission is required.')
            )
        
        # Only allow uploads for DRAFT or REVISION_REQUIRED submissions
        if submission.status not in [Submission.Status.DRAFT, Submission.Status.REVISION_REQUIRED]:
            raise serializers.ValidationError(
                _('Files can only be uploaded for draft or revision submissions.')
            )
        
        return attrs
    
    def create(self, validated_data):
        """Create file record."""
        submission = self.context['submission']
        user = self.context['request'].user
        
        validated_data['submission'] = submission
        validated_data['uploaded_by'] = user
        validated_data['original_filename'] = validated_data['file'].name
        
        # Set file size and mime type
        file = validated_data['file']
        validated_data['file_size'] = file.size
        validated_data['mime_type'] = file.content_type or ''
        
        return super().create(validated_data)


class FileReorderSerializer(serializers.Serializer):
    """
    Serializer for reordering files.
    """
    
    file_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        help_text=_('List of file IDs in the desired order')
    )
    
    def validate_file_ids(self, value):
        """Validate file IDs."""
        if not value:
            raise serializers.ValidationError(
                _('At least one file ID is required.')
            )
        
        # Check for duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                _('Duplicate file IDs are not allowed.')
            )
        
        return value
    
    def validate(self, attrs):
        """Validate that all files belong to the submission."""
        submission = self.context['submission']
        file_ids = attrs['file_ids']
        
        files = ManuscriptFile.objects.filter(
            id__in=file_ids,
            submission=submission,
            is_active=True
        )
        
        if files.count() != len(file_ids):
            raise serializers.ValidationError(
                _('Some file IDs do not belong to this submission.')
            )
        
        return attrs
