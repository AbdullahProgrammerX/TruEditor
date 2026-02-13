"""
TruEditor - File Service
=========================
Service layer for file operations with S3-compatible storage.
Handles upload validation, checksum calculation, and presigned URLs.

Developer: Abdullah Dogan
"""

import hashlib
import logging
import mimetypes
from typing import Optional
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .models import ManuscriptFile

logger = logging.getLogger(__name__)

# Max file size: 50MB
MAX_FILE_SIZE = getattr(settings, 'MAX_UPLOAD_SIZE', 50 * 1024 * 1024)

# Allowed extensions
ALLOWED_EXTENSIONS = {
    'doc', 'docx', 'pdf',
    'jpg', 'jpeg', 'png', 'tiff', 'tif',
    'xlsx', 'xls',
}


class FileService:
    """
    Centralized file management service.
    Works with both local and S3-compatible (Cloudflare R2) storage.
    """

    @staticmethod
    def validate_file(file: UploadedFile) -> dict:
        """
        Validate uploaded file.
        
        Returns:
            dict with 'valid' (bool) and 'error' (str|None)
        """
        # Check file size
        if file.size > MAX_FILE_SIZE:
            return {
                'valid': False,
                'error': f'File size ({file.size} bytes) exceeds maximum allowed ({MAX_FILE_SIZE} bytes).'
            }

        # Check extension
        ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if ext not in ALLOWED_EXTENSIONS:
            return {
                'valid': False,
                'error': f'File type .{ext} is not allowed. Allowed: {", ".join(sorted(ALLOWED_EXTENSIONS))}'
            }

        return {'valid': True, 'error': None}

    @staticmethod
    def calculate_checksum(file: UploadedFile) -> str:
        """
        Calculate SHA-256 checksum for the file.
        """
        sha256 = hashlib.sha256()
        file.seek(0)
        for chunk in file.chunks(chunk_size=8192):
            sha256.update(chunk)
        file.seek(0)  # Reset file pointer
        return sha256.hexdigest()

    @staticmethod
    def detect_mime_type(filename: str) -> str:
        """
        Detect MIME type from filename.
        """
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type or 'application/octet-stream'

    @staticmethod
    def get_presigned_url(file_instance: ManuscriptFile, expiration: int = 900) -> Optional[str]:
        """
        Generate a presigned download URL.
        
        Args:
            file_instance: ManuscriptFile instance
            expiration: URL validity in seconds (default 15 minutes)
            
        Returns:
            Presigned URL string or None
        """
        if not file_instance.file:
            return None

        try:
            storage = file_instance.file.storage
            
            # S3-compatible storage (boto3)
            if hasattr(storage, 'bucket'):
                return storage.url(file_instance.file.name, expire=expiration)
            
            # Local storage fallback
            return file_instance.file.url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for {file_instance.id}: {e}")
            return None

    @staticmethod
    def delete_file(file_instance: ManuscriptFile, hard: bool = False) -> bool:
        """
        Delete a file (soft or hard delete).
        
        Args:
            file_instance: ManuscriptFile instance
            hard: If True, permanently delete from storage
            
        Returns:
            True if successful
        """
        try:
            if hard:
                file_instance.hard_delete()
            else:
                file_instance.delete()
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_instance.id}: {e}")
            return False

    @staticmethod
    def reorder_files(submission, file_ids: list) -> bool:
        """
        Reorder files for a submission.
        
        Args:
            submission: Submission instance
            file_ids: Ordered list of file UUIDs
            
        Returns:
            True if successful
        """
        try:
            for order, file_id in enumerate(file_ids, start=1):
                ManuscriptFile.objects.filter(
                    id=file_id,
                    submission=submission,
                    is_active=True
                ).update(order=order)
            return True
        except Exception as e:
            logger.error(f"Failed to reorder files for submission {submission.id}: {e}")
            return False
