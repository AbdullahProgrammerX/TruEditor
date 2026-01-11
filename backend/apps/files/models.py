"""
TruEditor - File Models
=======================
Database models for file management.
Manuscript files (main text, cover letter, supplementary files, etc.)

Developer: Abdullah Dogan
"""

import os
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def manuscript_file_path(instance, filename):
    """
    Determine the upload path for files.
    Format: submissions/{submission_id}/{file_type}/{uuid}_{filename}
    """
    ext = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    
    if instance.submission:
        return f"submissions/{instance.submission.id}/{instance.file_type}/{unique_filename}"
    return f"temp/{unique_filename}"


class ManuscriptFile(models.Model):
    """
    Manuscript File Model.
    
    Manages files for each submission:
    - Main text (main_text)
    - Cover letter (cover_letter)
    - Tables (tables)
    - Figures (figures)
    - Supplementary files (supplementary)
    - Revision files (revision)
    """
    
    # ============================================
    # FILE TYPES
    # ============================================
    class FileType(models.TextChoices):
        MAIN_TEXT = 'main_text', _('Main Text')
        COVER_LETTER = 'cover_letter', _('Cover Letter')
        TITLE_PAGE = 'title_page', _('Title Page')
        ABSTRACT = 'abstract', _('Abstract')
        TABLES = 'tables', _('Tables')
        FIGURES = 'figures', _('Figures')
        SUPPLEMENTARY = 'supplementary', _('Supplementary Files')
        ETHICS_APPROVAL = 'ethics_approval', _('Ethics Approval Document')
        COPYRIGHT = 'copyright', _('Copyright Form')
        REVISION = 'revision', _('Revision File')
        REVISION_NOTES = 'revision_notes', _('Revision Notes')
        OTHER = 'other', _('Other')
    
    # ============================================
    # PRIMARY KEY
    # ============================================
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # ============================================
    # RELATIONS
    # ============================================
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Submission'),
        null=True,
        blank=True,
        help_text=_('Submission this file belongs to')
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files',
        verbose_name=_('Uploaded By'),
        help_text=_('User who uploaded the file')
    )
    
    # ============================================
    # FILE INFORMATION
    # ============================================
    file = models.FileField(
        _('File'),
        upload_to=manuscript_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'xlsx', 'xls']
            )
        ],
        help_text=_('Allowed formats: DOC, DOCX, PDF, JPG, PNG, TIFF, XLS, XLSX')
    )
    
    file_type = models.CharField(
        _('File Type'),
        max_length=30,
        choices=FileType.choices,
        default=FileType.OTHER,
        db_index=True,
        help_text=_('Type of the file')
    )
    
    original_filename = models.CharField(
        _('Original Filename'),
        max_length=255,
        help_text=_('Original name of the uploaded file')
    )
    
    file_size = models.PositiveIntegerField(
        _('File Size'),
        default=0,
        help_text=_('File size in bytes')
    )
    
    mime_type = models.CharField(
        _('MIME Type'),
        max_length=100,
        blank=True,
        help_text=_('MIME type of the file')
    )
    
    # ============================================
    # METADATA
    # ============================================
    description = models.CharField(
        _('Description'),
        max_length=500,
        blank=True,
        help_text=_('Brief description of the file')
    )
    
    caption = models.TextField(
        _('Caption'),
        blank=True,
        help_text=_('Figure/table caption')
    )
    
    order = models.PositiveSmallIntegerField(
        _('Order'),
        default=0,
        help_text=_('Display order of the files')
    )
    
    # ============================================
    # REVISION TRACKING
    # ============================================
    revision_number = models.PositiveSmallIntegerField(
        _('Revision Number'),
        default=0,
        help_text=_('Which revision this file belongs to')
    )
    
    replaces = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_by',
        verbose_name=_('Replaces'),
        help_text=_('Previous file that this file replaces')
    )
    
    # ============================================
    # STATUS
    # ============================================
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Is the file active? (False for deleted files)')
    )
    
    is_primary = models.BooleanField(
        _('Primary'),
        default=False,
        help_text=_('Is this the primary file of its type?')
    )
    
    # ============================================
    # SECURITY
    # ============================================
    checksum = models.CharField(
        _('Checksum'),
        max_length=64,
        blank=True,
        help_text=_('SHA-256 file checksum')
    )
    
    virus_scanned = models.BooleanField(
        _('Virus Scanned'),
        default=False,
        help_text=_('Has the file been scanned for viruses?')
    )
    
    virus_scan_date = models.DateTimeField(
        _('Virus Scan Date'),
        null=True,
        blank=True
    )
    
    # ============================================
    # TIMESTAMPS
    # ============================================
    created_at = models.DateTimeField(
        _('Uploaded At'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Manuscript File')
        verbose_name_plural = _('Manuscript Files')
        ordering = ['file_type', 'order', 'created_at']
        indexes = [
            models.Index(fields=['submission', 'file_type']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.original_filename} ({self.get_file_type_display()})"
    
    def save(self, *args, **kwargs):
        """Update file information before saving."""
        if self.file:
            # Original filename
            if not self.original_filename:
                self.original_filename = os.path.basename(self.file.name)
            
            # File size
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Soft delete - deactivate the file.
        Use hard_delete for permanent deletion.
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def hard_delete(self, *args, **kwargs):
        """Permanently delete the file."""
        # Delete from S3 as well
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Return the file extension."""
        if self.original_filename:
            return os.path.splitext(self.original_filename)[1].lower()
        return ''
    
    @property
    def file_size_human(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @property
    def is_image(self):
        """Check if the file is an image."""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp']
        return self.file_extension in image_extensions
    
    @property
    def is_document(self):
        """Check if the file is a document."""
        doc_extensions = ['.doc', '.docx', '.pdf', '.odt', '.rtf']
        return self.file_extension in doc_extensions
    
    def get_download_url(self, expiration=900):
        """
        Generate a presigned download URL.
        
        Args:
            expiration: URL validity period in seconds
        
        Returns:
            str: Download URL
        """
        # Use presigned URL for S3
        if hasattr(self.file.storage, 'url'):
            try:
                return self.file.storage.url(self.file.name, expire=expiration)
            except Exception:
                pass
        
        # Local storage
        return self.file.url if self.file else None


class FileDownloadLog(models.Model):
    """
    File Download Logs.
    For security and audit purposes.
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    file = models.ForeignKey(
        ManuscriptFile,
        on_delete=models.CASCADE,
        related_name='download_logs',
        verbose_name=_('File')
    )
    
    downloaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Downloaded By')
    )
    
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        null=True,
        blank=True
    )
    
    user_agent = models.TextField(
        _('User Agent'),
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('Downloaded At'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Download Log')
        verbose_name_plural = _('Download Logs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file.original_filename} - {self.downloaded_by} - {self.created_at}"
