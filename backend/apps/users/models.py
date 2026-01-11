"""
TruEditor - User Model
======================
ORCID tabanlı özel kullanıcı modeli.
Email/şifre ile kayıt YOKTUR, sadece ORCID ile giriş yapılır.

Geliştirici: Abdullah Doğan
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
    
    Alanlar:
    - ORCID bilgileri (zorunlu)
    - Kişisel bilgiler (ORCID'den + manuel)
    - İletişim bilgileri
    - Akademik bilgiler
    - Roller ve izinler
    """
    
    # ============================================
    # PRIMARY KEY
    # ============================================
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # ============================================
    # ORCID BİLGİLERİ (ZORUNLU)
    # ============================================
    orcid_id = models.CharField(
        _('ORCID ID'),
        max_length=19,  # Format: 0000-0000-0000-0000
        unique=True,
        db_index=True,
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
    
    orcid_token_expires = models.DateTimeField(
        _('Token Bitiş Tarihi'),
        null=True,
        blank=True,
        help_text=_('ORCID access token ne zaman sona eriyor')
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
    
    # ============================================
    # KİŞİSEL BİLGİLER
    # ============================================
    email = models.EmailField(
        _('Email Adresi'),
        blank=True,
        null=True,
        db_index=True,
        help_text=_('İletişim email adresi')
    )
    
    full_name = models.CharField(
        _('Ad Soyad'),
        max_length=255,
        blank=True,
        help_text=_('Tam ad')
    )
    
    given_name = models.CharField(
        _('Ad'),
        max_length=100,
        blank=True,
        help_text=_('Ad')
    )
    
    family_name = models.CharField(
        _('Soyad'),
        max_length=100,
        blank=True,
        help_text=_('Soyad')
    )
    
    # ============================================
    # İLETİŞİM BİLGİLERİ
    # ============================================
    phone = models.CharField(
        _('Telefon'),
        max_length=20,
        blank=True,
        help_text=_('İletişim telefon numarası')
    )
    
    country = models.CharField(
        _('Ülke'),
        max_length=100,
        blank=True,
        help_text=_('Ülke')
    )
    
    city = models.CharField(
        _('Şehir'),
        max_length=100,
        blank=True,
        help_text=_('Şehir')
    )
    
    address = models.TextField(
        _('Adres'),
        blank=True,
        help_text=_('Posta adresi')
    )
    
    # ============================================
    # AKADEMİK BİLGİLER
    # ============================================
    title = models.CharField(
        _('Unvan'),
        max_length=50,
        blank=True,
        choices=[
            ('', _('Seçiniz')),
            ('prof_dr', _('Prof. Dr.')),
            ('doc_dr', _('Doç. Dr.')),
            ('dr_ogr_uyesi', _('Dr. Öğr. Üyesi')),
            ('dr', _('Dr.')),
            ('ogr_gor', _('Öğr. Gör.')),
            ('ars_gor', _('Arş. Gör.')),
            ('uzman', _('Uzman')),
            ('ogrenci', _('Öğrenci')),
            ('diger', _('Diğer')),
        ],
        help_text=_('Akademik unvan')
    )
    
    institution = models.CharField(
        _('Kurum'),
        max_length=255,
        blank=True,
        help_text=_('Bağlı olduğu kurum')
    )
    
    department = models.CharField(
        _('Departman/Bölüm'),
        max_length=255,
        blank=True,
        help_text=_('Departman veya bölüm')
    )
    
    expertise_areas = models.JSONField(
        _('Uzmanlık Alanları'),
        default=list,
        blank=True,
        help_text=_('Uzmanlık alanları listesi')
    )
    
    bio = models.TextField(
        _('Biyografi'),
        blank=True,
        max_length=1000,
        help_text=_('Kısa biyografi (maks. 1000 karakter)')
    )
    
    website = models.URLField(
        _('Web Sitesi'),
        blank=True,
        help_text=_('Kişisel veya kurumsal web sitesi')
    )
    
    # ============================================
    # ROLLER VE İZİNLER
    # ============================================
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
    
    is_chief_editor = models.BooleanField(
        _('Baş Editör mü?'),
        default=False,
        help_text=_('Kullanıcı baş editör mü?')
    )
    
    reviewer_interests = models.JSONField(
        _('Hakemlik İlgi Alanları'),
        default=list,
        blank=True,
        help_text=_('Hakemlik yapmak istediği alanlar')
    )
    
    # ============================================
    # DJANGO STANDART ALANLARI
    # ============================================
    is_staff = models.BooleanField(
        _('Personel'),
        default=False,
        help_text=_('Kullanıcı admin paneline erişebilir mi?')
    )
    
    is_active = models.BooleanField(
        _('Aktif'),
        default=True,
        db_index=True,
        help_text=_('Kullanıcı hesabı aktif mi?')
    )
    
    email_verified = models.BooleanField(
        _('Email Doğrulandı'),
        default=False,
        help_text=_('Email adresi doğrulandı mı?')
    )
    
    profile_completed = models.BooleanField(
        _('Profil Tamamlandı'),
        default=False,
        help_text=_('Kullanıcı profil bilgilerini doldurdu mu?')
    )
    
    # ============================================
    # ZAMAN DAMGALARI
    # ============================================
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
    
    # ============================================
    # MANAGER
    # ============================================
    objects = UserManager()
    
    # Authentication ayarları
    USERNAME_FIELD = 'orcid_id'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('Kullanıcı')
        verbose_name_plural = _('Kullanıcılar')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['orcid_id']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_reviewer']),
            models.Index(fields=['is_editor']),
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
    
    @property
    def display_name(self):
        """Görüntüleme adını döndürür."""
        if self.title and self.full_name:
            return f"{self.get_title_display()} {self.full_name}"
        return self.get_full_name()
    
    def check_profile_completion(self):
        """
        Profil tamamlanma durumunu kontrol eder.
        Zorunlu alanlar dolu mu?
        """
        required_fields = ['full_name', 'email', 'institution']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True
    
    def update_profile_completion(self):
        """Profil tamamlanma durumunu günceller."""
        self.profile_completed = self.check_profile_completion()
        self.save(update_fields=['profile_completed', 'updated_at'])
    
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
        if emails and not self.email:
            # Birincil veya doğrulanmış emaili tercih et
            for email in emails:
                if email.get('primary') or email.get('verified'):
                    self.email = email.get('email')
                    break
            if not self.email and emails:
                self.email = emails[0].get('email')
        
        # Ülke
        addresses = person.get('addresses', {}).get('address', [])
        if addresses and not self.country:
            self.country = addresses[0].get('country', {}).get('value', '')
        
        # Kurum bilgisi (aktivitelerden)
        activities = orcid_data.get('activities-summary', {})
        employments = activities.get('employments', {}).get('affiliation-group', [])
        
        if employments and not self.institution:
            for group in employments:
                summaries = group.get('summaries', [])
                if summaries:
                    employment = summaries[0].get('employment-summary', {})
                    org = employment.get('organization', {})
                    self.institution = org.get('name', '')
                    
                    dept = employment.get('department-name')
                    if dept and not self.department:
                        self.department = dept
                    break
        
        # Biyografi
        biography = person.get('biography', {})
        if biography and not self.bio:
            self.bio = biography.get('content', '')[:1000]
        
        # Web sitesi
        researcher_urls = person.get('researcher-urls', {}).get('researcher-url', [])
        if researcher_urls and not self.website:
            self.website = researcher_urls[0].get('url', {}).get('value', '')
        
        # Ham veriyi sakla
        self.orcid_data = orcid_data
        self.last_orcid_sync = timezone.now()
        
        # Profil tamamlanma durumunu güncelle
        self.profile_completed = self.check_profile_completion()
        
        self.save()
