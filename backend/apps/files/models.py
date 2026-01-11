"""
TruEditor - File Models
=======================
Dosya yönetimi için veritabanı modelleri.
Makale dosyaları (ana metin, kapak mektubu, ek dosyalar, vb.)

Geliştirici: Abdullah Doğan
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
    Dosya yükleme yolunu belirler.
    Format: submissions/{submission_id}/{file_type}/{uuid}_{filename}
    """
    ext = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    
    if instance.submission:
        return f"submissions/{instance.submission.id}/{instance.file_type}/{unique_filename}"
    return f"temp/{unique_filename}"


class ManuscriptFile(models.Model):
    """
    Makale Dosya Modeli.
    
    Her gönderime ait dosyaları yönetir:
    - Ana metin (main_text)
    - Kapak mektubu (cover_letter)
    - Tablolar (tables)
    - Şekiller (figures)
    - Ek dosyalar (supplementary)
    - Revizyon dosyaları (revision)
    """
    
    # ============================================
    # DOSYA TÜRLERİ
    # ============================================
    class FileType(models.TextChoices):
        MAIN_TEXT = 'main_text', _('Ana Metin')
        COVER_LETTER = 'cover_letter', _('Kapak Mektubu')
        TITLE_PAGE = 'title_page', _('Başlık Sayfası')
        ABSTRACT = 'abstract', _('Özet')
        TABLES = 'tables', _('Tablolar')
        FIGURES = 'figures', _('Şekiller')
        SUPPLEMENTARY = 'supplementary', _('Ek Dosyalar')
        ETHICS_APPROVAL = 'ethics_approval', _('Etik Onay Belgesi')
        COPYRIGHT = 'copyright', _('Telif Hakkı Formu')
        REVISION = 'revision', _('Revizyon Dosyası')
        REVISION_NOTES = 'revision_notes', _('Revizyon Açıklamaları')
        OTHER = 'other', _('Diğer')
    
    # ============================================
    # PRIMARY KEY
    # ============================================
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # ============================================
    # İLİŞKİLER
    # ============================================
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Gönderim'),
        null=True,
        blank=True,
        help_text=_('Bu dosyanın ait olduğu gönderim')
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files',
        verbose_name=_('Yükleyen'),
        help_text=_('Dosyayı yükleyen kullanıcı')
    )
    
    # ============================================
    # DOSYA BİLGİLERİ
    # ============================================
    file = models.FileField(
        _('Dosya'),
        upload_to=manuscript_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['doc', 'docx', 'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif', 'xlsx', 'xls']
            )
        ],
        help_text=_('İzin verilen formatlar: DOC, DOCX, PDF, JPG, PNG, TIFF, XLS, XLSX')
    )
    
    file_type = models.CharField(
        _('Dosya Türü'),
        max_length=30,
        choices=FileType.choices,
        default=FileType.OTHER,
        db_index=True,
        help_text=_('Dosyanın türü')
    )
    
    original_filename = models.CharField(
        _('Orijinal Dosya Adı'),
        max_length=255,
        help_text=_('Yüklenen dosyanın orijinal adı')
    )
    
    file_size = models.PositiveIntegerField(
        _('Dosya Boyutu'),
        default=0,
        help_text=_('Dosya boyutu (byte)')
    )
    
    mime_type = models.CharField(
        _('MIME Tipi'),
        max_length=100,
        blank=True,
        help_text=_('Dosyanın MIME tipi')
    )
    
    # ============================================
    # META BİLGİLER
    # ============================================
    description = models.CharField(
        _('Açıklama'),
        max_length=500,
        blank=True,
        help_text=_('Dosya hakkında kısa açıklama')
    )
    
    caption = models.TextField(
        _('Altyazı'),
        blank=True,
        help_text=_('Şekil/tablo altyazısı')
    )
    
    order = models.PositiveSmallIntegerField(
        _('Sıra'),
        default=0,
        help_text=_('Dosyaların görüntülenme sırası')
    )
    
    # ============================================
    # REVİZYON TAKİBİ
    # ============================================
    revision_number = models.PositiveSmallIntegerField(
        _('Revizyon Numarası'),
        default=0,
        help_text=_('Bu dosya hangi revizyona ait')
    )
    
    replaces = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replaced_by',
        verbose_name=_('Değiştirdiği Dosya'),
        help_text=_('Bu dosyanın yerine geçtiği önceki dosya')
    )
    
    # ============================================
    # DURUM
    # ============================================
    is_active = models.BooleanField(
        _('Aktif'),
        default=True,
        help_text=_('Dosya aktif mi? (Silinen dosyalar için False)')
    )
    
    is_primary = models.BooleanField(
        _('Birincil'),
        default=False,
        help_text=_('Bu türdeki birincil dosya mı?')
    )
    
    # ============================================
    # GÜVENLİK
    # ============================================
    checksum = models.CharField(
        _('Checksum'),
        max_length=64,
        blank=True,
        help_text=_('SHA-256 dosya checksum\'u')
    )
    
    virus_scanned = models.BooleanField(
        _('Virüs Tarandı'),
        default=False,
        help_text=_('Dosya virüs taramasından geçti mi?')
    )
    
    virus_scan_date = models.DateTimeField(
        _('Virüs Tarama Tarihi'),
        null=True,
        blank=True
    )
    
    # ============================================
    # ZAMAN DAMGALARI
    # ============================================
    created_at = models.DateTimeField(
        _('Yükleme Tarihi'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Makale Dosyası')
        verbose_name_plural = _('Makale Dosyaları')
        ordering = ['file_type', 'order', 'created_at']
        indexes = [
            models.Index(fields=['submission', 'file_type']),
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.original_filename} ({self.get_file_type_display()})"
    
    def save(self, *args, **kwargs):
        """Kaydetmeden önce dosya bilgilerini güncelle."""
        if self.file:
            # Orijinal dosya adı
            if not self.original_filename:
                self.original_filename = os.path.basename(self.file.name)
            
            # Dosya boyutu
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Soft delete - dosyayı deaktif et.
        Gerçek silme için hard_delete kullan.
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def hard_delete(self, *args, **kwargs):
        """Dosyayı kalıcı olarak sil."""
        # S3'ten de sil
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Dosya uzantısını döndür."""
        if self.original_filename:
            return os.path.splitext(self.original_filename)[1].lower()
        return ''
    
    @property
    def file_size_human(self):
        """İnsan okunabilir dosya boyutu."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @property
    def is_image(self):
        """Dosya bir görsel mi?"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp']
        return self.file_extension in image_extensions
    
    @property
    def is_document(self):
        """Dosya bir döküman mı?"""
        doc_extensions = ['.doc', '.docx', '.pdf', '.odt', '.rtf']
        return self.file_extension in doc_extensions
    
    def get_download_url(self, expiration=900):
        """
        Presigned download URL oluştur.
        
        Args:
            expiration: URL geçerlilik süresi (saniye)
        
        Returns:
            str: Download URL
        """
        # S3 kullanılıyorsa presigned URL
        if hasattr(self.file.storage, 'url'):
            try:
                return self.file.storage.url(self.file.name, expire=expiration)
            except Exception:
                pass
        
        # Local storage
        return self.file.url if self.file else None


class FileDownloadLog(models.Model):
    """
    Dosya İndirme Logları.
    Güvenlik ve denetim için.
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
        verbose_name=_('Dosya')
    )
    
    downloaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('İndiren')
    )
    
    ip_address = models.GenericIPAddressField(
        _('IP Adresi'),
        null=True,
        blank=True
    )
    
    user_agent = models.TextField(
        _('User Agent'),
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('İndirme Tarihi'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('İndirme Logu')
        verbose_name_plural = _('İndirme Logları')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.file.original_filename} - {self.downloaded_by} - {self.created_at}"
