"""
TruEditor - User Model
======================
ORCID tabanlı özel kullanıcı modeli.
Email/şifre ile kayıt YOKTUR, sadece ORCID ile giriş yapılır.
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    ORCID tabanlı kullanıcı yöneticisi.
    """
    
    def create_user(self, orcid_id, email=None, **extra_fields):
        """
        ORCID ID ile yeni kullanıcı oluşturur.
        
        Args:
            orcid_id: ORCID tanımlayıcısı (zorunlu)
            email: Email adresi (opsiyonel, ORCID'den çekilir)
            **extra_fields: Diğer alanlar
        
        Returns:
            User: Oluşturulan kullanıcı
        """
        if not orcid_id:
            raise ValueError(_('ORCID ID zorunludur'))
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            orcid_id=orcid_id,
            email=email,
            **extra_fields
        )
        # ORCID kullanıcıları için şifre belirlenmez
        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, orcid_id, email=None, password=None, **extra_fields):
        """
        Süper kullanıcı oluşturur.
        Not: Admin paneli için şifre gereklidir.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser is_staff=True olmalı'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser is_superuser=True olmalı'))
        
        user = self.create_user(orcid_id, email, **extra_fields)
        
        # Admin için şifre belirle
        if password:
            user.set_password(password)
            user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    TruEditor Özel Kullanıcı Modeli.
    
    ORCID ID ile kimlik doğrulama yapar.
    Email/şifre ile kayıt YOKTUR.
    """
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # ORCID Bilgileri (ZORUNLU)
    orcid_id = models.CharField(
        _('ORCID ID'),
        max_length=19,  # Format: 0000-0000-0000-0000
        unique=True,
        help_text=_('ORCID tanımlayıcısı (örn: 0000-0002-1825-0097)')
    )
    
    orcid_access_token = models.TextField(
        _('ORCID Access Token'),
        blank=True,
        null=True,
        help_text=_('ORCID API erişim tokeni')
    )
    
    orcid_refresh_token = models.TextField(
        _('ORCID Refresh Token'),
        blank=True,
        null=True,
        help_text=_('ORCID token yenileme tokeni')
    )
    
    orcid_data = models.JSONField(
        _('ORCID Profil Verileri'),
        default=dict,
        blank=True,
        help_text=_('ORCID API\'den çekilen tam profil verisi')
    )
    
    last_orcid_sync = models.DateTimeField(
        _('Son ORCID Senkronizasyonu'),
        null=True,
        blank=True,
        help_text=_('ORCID profili en son ne zaman senkronize edildi')
    )
    
    # Temel Kullanıcı Bilgileri
    email = models.EmailField(
        _('Email Adresi'),
        blank=True,
        null=True,
        help_text=_('ORCID\'den çekilen email adresi')
    )
    
    full_name = models.CharField(
        _('Ad Soyad'),
        max_length=255,
        blank=True,
        help_text=_('ORCID\'den çekilen tam ad')
    )
    
    given_name = models.CharField(
        _('Ad'),
        max_length=100,
        blank=True,
        help_text=_('ORCID\'den çekilen ad')
    )
    
    family_name = models.CharField(
        _('Soyad'),
        max_length=100,
        blank=True,
        help_text=_('ORCID\'den çekilen soyad')
    )
    
    # Kurum Bilgileri
    institution = models.CharField(
        _('Kurum'),
        max_length=255,
        blank=True,
        help_text=_('ORCID\'den çekilen kurum bilgisi')
    )
    
    department = models.CharField(
        _('Departman'),
        max_length=255,
        blank=True,
        help_text=_('ORCID\'den çekilen departman bilgisi')
    )
    
    # Roller ve İzinler
    is_reviewer = models.BooleanField(
        _('Hakem mi?'),
        default=False,
        help_text=_('Kullanıcı hakem olarak görev yapabilir mi?')
    )
    
    is_editor = models.BooleanField(
        _('Editör mü?'),
        default=False,
        help_text=_('Kullanıcı editör olarak görev yapabilir mi?')
    )
    
    # Django Standart Alanları
    is_staff = models.BooleanField(
        _('Personel'),
        default=False,
        help_text=_('Kullanıcı admin paneline erişebilir mi?')
    )
    
    is_active = models.BooleanField(
        _('Aktif'),
        default=True,
        help_text=_('Kullanıcı hesabı aktif mi?')
    )
    
    # Zaman Damgaları
    date_joined = models.DateTimeField(
        _('Kayıt Tarihi'),
        default=timezone.now
    )
    
    last_login = models.DateTimeField(
        _('Son Giriş'),
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('Oluşturulma Tarihi'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'),
        auto_now=True
    )
    
    # Manager
    objects = UserManager()
    
    # Authentication ayarları
    USERNAME_FIELD = 'orcid_id'
    REQUIRED_FIELDS = []  # createsuperuser için ek alan yok
    
    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['orcid_id']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        """Kullanıcıyı temsil eden string."""
        if self.full_name:
            return f"{self.full_name} ({self.orcid_id})"
        return self.orcid_id
    
    def get_full_name(self):
        """Tam adı döndürür."""
        if self.full_name:
            return self.full_name
        if self.given_name or self.family_name:
            return f"{self.given_name} {self.family_name}".strip()
        return self.orcid_id
    
    def get_short_name(self):
        """Kısa adı (ad) döndürür."""
        return self.given_name or self.orcid_id
    
    @property
    def orcid_url(self):
        """ORCID profil URL'ini döndürür."""
        return f"https://orcid.org/{self.orcid_id}"
    
    def update_from_orcid(self, orcid_data: dict):
        """
        ORCID API'den gelen verilerle kullanıcı profilini günceller.
        
        Args:
            orcid_data: ORCID API'den dönen profil verisi
        """
        # Person bilgileri
        person = orcid_data.get('person', {})
        name = person.get('name', {})
        
        # Ad Soyad
        if name.get('given-names'):
            self.given_name = name['given-names'].get('value', '')
        if name.get('family-name'):
            self.family_name = name['family-name'].get('value', '')
        
        self.full_name = f"{self.given_name} {self.family_name}".strip()
        
        # Email
        emails = person.get('emails', {}).get('email', [])
        if emails:
            # Birincil veya doğrulanmış emaili tercih et
            for email in emails:
                if email.get('primary') or email.get('verified'):
                    self.email = email.get('email')
                    break
            if not self.email and emails:
                self.email = emails[0].get('email')
        
        # Kurum bilgisi (aktivitelerden)
        activities = orcid_data.get('activities-summary', {})
        employments = activities.get('employments', {}).get('employment-summary', [])
        if employments:
            latest = employments[0]
            org = latest.get('organization', {})
            self.institution = org.get('name', '')
            
            dept = latest.get('department-name')
            if dept:
                self.department = dept
        
        # Ham veriyi sakla
        self.orcid_data = orcid_data
        self.last_orcid_sync = timezone.now()
        
        self.save()
