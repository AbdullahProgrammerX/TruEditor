"""
TruEditor - File Views
======================
API views for file upload and management.

Developer: Abdullah Dogan
"""

import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import ManuscriptFile
from .serializers import (
    ManuscriptFileSerializer,
    FileUploadSerializer,
    FileReorderSerializer,
)
from apps.submissions.models import Submission
from apps.common.response import (
    success_response,
    error_response,
    created_response,
    validation_error_response,
    not_found_response,
    forbidden_response,
)

logger = logging.getLogger(__name__)


class ManuscriptFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing manuscript files.
    
    Actions:
    - list: Get files for a submission
    - create: Upload a new file
    - destroy: Delete a file (soft delete)
    - reorder: Reorder files
    - presigned_url: Get download URL
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = ManuscriptFileSerializer
    
    def get_queryset(self):
        """
        Return files for the specified submission.
        """
        submission_id = self.request.query_params.get('submission_id')
        
        if not submission_id:
            return ManuscriptFile.objects.none()
        
        # Get submission and check ownership
        submission = get_object_or_404(Submission, id=submission_id)
        
        # Only owner can access files
        if submission.submitter != self.request.user:
            return ManuscriptFile.objects.none()
        
        return ManuscriptFile.objects.filter(
            submission=submission,
            is_active=True
        ).order_by('file_type', 'order', 'created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return FileUploadSerializer
        return ManuscriptFileSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List files for a submission.
        
        Query params:
        - submission_id: Submission UUID (required)
        """
        submission_id = request.query_params.get('submission_id')
        
        if not submission_id:
            return validation_error_response(
                _('submission_id parameter is required.')
            )
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return success_response(
            data=serializer.data,
            message=_('Files retrieved successfully')
        )
    
    def create(self, request, *args, **kwargs):
        """
        Upload a new file.
        
        Required fields:
        - file: File to upload
        - file_type: Type of file
        - submission_id: Submission UUID (query param)
        """
        submission_id = request.query_params.get('submission_id')
        
        if not submission_id:
            return validation_error_response(
                _('submission_id parameter is required.')
            )
        
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return not_found_response(
                _('Submission not found.')
            )
        
        # Check ownership
        if submission.submitter != request.user:
            return forbidden_response(
                _('You do not have permission to upload files for this submission.')
            )
        
        # Check submission status
        if not submission.is_editable:
            return validation_error_response(
                _('Files can only be uploaded for draft or revision submissions.')
            )
        
        serializer = self.get_serializer(
            data=request.data,
            context={
                'request': request,
                'submission': submission
            }
        )
        serializer.is_valid(raise_exception=True)
        file_instance = serializer.save()
        
        return created_response(
            data=ManuscriptFileSerializer(file_instance).data,
            message=_('File uploaded successfully')
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a file (soft delete).
        """
        instance = self.get_object()
        
        # Check ownership through submission
        if instance.submission and instance.submission.submitter != request.user:
            return forbidden_response(
                _('You do not have permission to delete this file.')
            )
        
        # Soft delete
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        """
        Reorder files for a submission.
        
        Request body:
        {
            "file_ids": ["uuid1", "uuid2", ...]
        }
        """
        instance = self.get_object()
        submission = instance.submission
        
        if not submission:
            return validation_error_response(
                _('File must belong to a submission.')
            )
        
        # Check ownership
        if submission.submitter != request.user:
            return forbidden_response(
                _('You do not have permission to reorder files for this submission.')
            )
        
        serializer = FileReorderSerializer(
            data=request.data,
            context={'submission': submission}
        )
        serializer.is_valid(raise_exception=True)
        
        file_ids = serializer.validated_data['file_ids']
        
        # Update order
        for order, file_id in enumerate(file_ids, start=1):
            ManuscriptFile.objects.filter(
                id=file_id,
                submission=submission
            ).update(order=order)
        
        # Return updated file list
        files = ManuscriptFile.objects.filter(
            submission=submission,
            is_active=True
        ).order_by('order')
        
        return success_response(
            data=ManuscriptFileSerializer(files, many=True).data,
            message=_('Files reordered successfully')
        )
    
    @action(detail=True, methods=['get'])
    def presigned_url(self, request, pk=None):
        """
        Get presigned download URL for a file.
        
        Returns a temporary URL valid for 15 minutes.
        """
        instance = self.get_object()
        
        # Check ownership through submission
        if instance.submission and instance.submission.submitter != request.user:
            return forbidden_response(
                _('You do not have permission to access this file.')
            )
        
        try:
            download_url = instance.get_download_url(expiration=900)  # 15 minutes
            
            return success_response(
                data={
                    'file_id': str(instance.id),
                    'download_url': download_url,
                    'expires_in': 900,
                    'filename': instance.original_filename
                },
                message=_('Download URL generated successfully')
            )
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return error_response(
                message=_('Failed to generate download URL'),
                code='URL_GENERATION_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
