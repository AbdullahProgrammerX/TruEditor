"""
TruEditor - Submission Models
=============================
Makale gönderimleri için veritabanı modelleri.
FSM (Finite State Machine) ile durum yönetimi.

Geliştirici: Abdullah Doğan
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django_fsm import FSMField, transition


class Submission(models.Model):
    """
    Makale Gönderimi Modeli.
    
    Bir makale gönderiminin tüm yaşam döngüsünü yönetir:
    - draft → submitted → under_review → revision_required → accepted/rejected
    
    İlişkiler:
    - User (submitter): Gönderimi yapan kullanıcı
    - Author: Yazarlar (sıralı liste)
    - ManuscriptFile: Yüklenen dosyalar
    """
    
    # ============================================
    # DURUM SEÇENEKLERİ
    # ============================================
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Taslak')
        SUBMITTED = 'submitted', _('Gönderildi')
        UNDER_REVIEW = 'under_review', _('İncelemede')
        REVISION_REQUIRED = 'revision_required', _('Revizyon Gerekli')
        REVISION_SUBMITTED = 'revision_submitted', _('Revizyon Gönderildi')
        ACCEPTED = 'accepted', _('Kabul Edildi')
        REJECTED = 'rejected', _('Reddedildi')
        WITHDRAWN = 'withdrawn', _('Geri Çekildi')
        PUBLISHED = 'published', _('Yayınlandı')
    
    # ============================================
    # MAKALE TÜRLERİ
    # ============================================
    class ArticleType(models.TextChoices):
        RESEARCH = 'research', _('Araştırma Makalesi')
        REVIEW = 'review', _('Derleme')
        CASE_REPORT = 'case_report', _('Olgu Sunumu')
        SHORT_COMM = 'short_communication', _('Kısa Bildiri')
        LETTER = 'letter', _('Editöre Mektup')
        EDITORIAL = 'editorial', _('Editöryal')
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
    # GÖNDERİM BİLGİLERİ
    # ============================================
    manuscript_id = models.CharField(
        _('Makale Numarası'),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Otomatik oluşturulan makale numarası (örn: TRU-2026-0001)')
    )
    
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='submissions',
        verbose_name=_('Gönderen'),
        help_text=_('Makaleyi sisteme gönderen kullanıcı')
    )
    
    # ============================================
    # DURUM (FSM)
    # ============================================
    status = FSMField(
        _('Durum'),
        default=Status.DRAFT,
        choices=Status.choices,
        db_index=True,
        protected=True,  # Sadece transition'larla değiştirilebilir
        help_text=_('Makalenin mevcut durumu')
    )
    
    # ============================================
    # MAKALE BİLGİLERİ
    # ============================================
    title = models.CharField(
        _('Başlık'),
        max_length=500,
        help_text=_('Makalenin başlığı')
    )
    
    title_en = models.CharField(
        _('İngilizce Başlık'),
        max_length=500,
        blank=True,
        help_text=_('Makalenin İngilizce başlığı (opsiyonel)')
    )
    
    abstract = models.TextField(
        _('Özet'),
        max_length=5000,
        help_text=_('Makalenin özeti (maks. 5000 karakter)')
    )
    
    abstract_en = models.TextField(
        _('İngilizce Özet'),
        max_length=5000,
        blank=True,
        help_text=_('İngilizce özet (opsiyonel)')
    )
    
    keywords = models.JSONField(
        _('Anahtar Kelimeler'),
        default=list,
        help_text=_('Anahtar kelimeler listesi')
    )
    
    keywords_en = models.JSONField(
        _('İngilizce Anahtar Kelimeler'),
        default=list,
        blank=True,
        help_text=_('İngilizce anahtar kelimeler')
    )
    
    article_type = models.CharField(
        _('Makale Türü'),
        max_length=30,
        choices=ArticleType.choices,
        default=ArticleType.RESEARCH,
        help_text=_('Makalenin türü')
    )
    
    language = models.CharField(
        _('Dil'),
        max_length=5,
        default='tr',
        choices=[
            ('tr', _('Türkçe')),
            ('en', _('İngilizce')),
        ],
        help_text=_('Makalenin yazıldığı dil')
    )
    
    # ============================================
    # KAPAK MEKTUBU VE ETİK
    # ============================================
    cover_letter = models.TextField(
        _('Kapak Mektubu'),
        blank=True,
        help_text=_('Editöre kapak mektubu')
    )
    
    ethics_statement = models.TextField(
        _('Etik Beyanı'),
        blank=True,
        help_text=_('Etik kurul onayı ve beyanı')
    )
    
    ethics_approval_number = models.CharField(
        _('Etik Kurul Onay Numarası'),
        max_length=100,
        blank=True,
        help_text=_('Etik kurul onay numarası (varsa)')
    )
    
    conflict_of_interest = models.TextField(
        _('Çıkar Çatışması Beyanı'),
        blank=True,
        help_text=_('Çıkar çatışması beyanı')
    )
    
    funding_statement = models.TextField(
        _('Finansman Beyanı'),
        blank=True,
        help_text=_('Araştırma finansmanı bilgisi')
    )
    
    # ============================================
    # WIZARD İLERLEMESİ
    # ============================================
    wizard_step = models.PositiveSmallIntegerField(
        _('Wizard Adımı'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text=_('Gönderim wizard\'ında şu anki adım (1-6)')
    )
    
    wizard_data = models.JSONField(
        _('Wizard Verileri'),
        default=dict,
        blank=True,
        help_text=_('Wizard adımlarından toplanan geçici veriler')
    )
    
    # ============================================
    # REVİZYON BİLGİLERİ
    # ============================================
    revision_number = models.PositiveSmallIntegerField(
        _('Revizyon Numarası'),
        default=0,
        help_text=_('Kaçıncı revizyon')
    )
    
    revision_notes = models.TextField(
        _('Revizyon Notları'),
        blank=True,
        help_text=_('Editör revizyon talep notları')
    )
    
    revision_deadline = models.DateTimeField(
        _('Revizyon Son Tarihi'),
        null=True,
        blank=True,
        help_text=_('Revizyon teslim tarihi')
    )
    
    # ============================================
    # EDİTÖR ATAMASI
    # ============================================
    assigned_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='editor_submissions',
        verbose_name=_('Atanan Editör'),
        help_text=_('Makaleyi değerlendiren editör')
    )
    
    editor_notes = models.TextField(
        _('Editör Notları'),
        blank=True,
        help_text=_('Editörün dahili notları')
    )
    
    editor_decision = models.CharField(
        _('Editör Kararı'),
        max_length=50,
        blank=True,
        choices=[
            ('accept', _('Kabul')),
            ('minor_revision', _('Küçük Revizyon')),
            ('major_revision', _('Büyük Revizyon')),
            ('reject', _('Red')),
        ],
        help_text=_('Editörün nihai kararı')
    )
    
    editor_decision_date = models.DateTimeField(
        _('Karar Tarihi'),
        null=True,
        blank=True,
        help_text=_('Editör kararının verildiği tarih')
    )
    
    # ============================================
    # ZAMAN DAMGALARI
    # ============================================
    created_at = models.DateTimeField(
        _('Oluşturulma Tarihi'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'),
        auto_now=True
    )
    
    submitted_at = models.DateTimeField(
        _('Gönderim Tarihi'),
        null=True,
        blank=True,
        help_text=_('Makalenin ilk gönderildiği tarih')
    )
    
    accepted_at = models.DateTimeField(
        _('Kabul Tarihi'),
        null=True,
        blank=True,
        help_text=_('Makalenin kabul edildiği tarih')
    )
    
    published_at = models.DateTimeField(
        _('Yayın Tarihi'),
        null=True,
        blank=True,
        help_text=_('Makalenin yayınlandığı tarih')
    )
    
    class Meta:
        verbose_name = _('Gönderim')
        verbose_name_plural = _('Gönderimler')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['manuscript_id']),
            models.Index(fields=['status']),
            models.Index(fields=['submitter']),
            models.Index(fields=['assigned_editor']),
            models.Index(fields=['created_at']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.manuscript_id or 'DRAFT'}: {self.title[:50]}"
    
    def save(self, *args, **kwargs):
        """Kaydetmeden önce manuscript_id oluştur."""
        if not self.manuscript_id and self.status != self.Status.DRAFT:
            self.manuscript_id = self.generate_manuscript_id()
        super().save(*args, **kwargs)
    
    def generate_manuscript_id(self):
        """
        Benzersiz makale numarası oluşturur.
        Format: TRU-YYYY-NNNN
        """
        year = timezone.now().year
        prefix = f"TRU-{year}-"
        
        # Bu yıla ait son numarayı bul
        last_submission = Submission.objects.filter(
            manuscript_id__startswith=prefix
        ).order_by('-manuscript_id').first()
        
        if last_submission:
            try:
                last_number = int(last_submission.manuscript_id.split('-')[-1])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        return f"{prefix}{new_number:04d}"
    
    # ============================================
    # FSM DURUM GEÇİŞLERİ
    # ============================================
    
    @transition(field=status, source=Status.DRAFT, target=Status.SUBMITTED)
    def submit(self):
        """
        Taslağı gönder.
        Validasyonlar transition öncesi yapılmalı.
        """
        self.submitted_at = timezone.now()
        self.manuscript_id = self.generate_manuscript_id()
    
    @transition(field=status, source=Status.SUBMITTED, target=Status.UNDER_REVIEW)
    def start_review(self, editor):
        """
        İnceleme sürecini başlat.
        
        Args:
            editor: Atanan editör
        """
        self.assigned_editor = editor
    
    @transition(
        field=status,
        source=[Status.UNDER_REVIEW, Status.REVISION_SUBMITTED],
        target=Status.REVISION_REQUIRED
    )
    def request_revision(self, notes, deadline_days=30):
        """
        Revizyon talep et.
        
        Args:
            notes: Revizyon notları
            deadline_days: Revizyon için gün sayısı
        """
        self.revision_notes = notes
        self.revision_deadline = timezone.now() + timezone.timedelta(days=deadline_days)
        self.revision_number += 1
    
    @transition(field=status, source=Status.REVISION_REQUIRED, target=Status.REVISION_SUBMITTED)
    def submit_revision(self):
        """Revizyonu gönder."""
        pass
    
    @transition(
        field=status,
        source=[Status.UNDER_REVIEW, Status.REVISION_SUBMITTED],
        target=Status.ACCEPTED
    )
    def accept(self, decision_notes=''):
        """
        Makaleyi kabul et.
        
        Args:
            decision_notes: Karar notları
        """
        self.editor_decision = 'accept'
        self.editor_notes = decision_notes
        self.editor_decision_date = timezone.now()
        self.accepted_at = timezone.now()
    
    @transition(
        field=status,
        source=[Status.SUBMITTED, Status.UNDER_REVIEW, Status.REVISION_SUBMITTED],
        target=Status.REJECTED
    )
    def reject(self, decision_notes=''):
        """
        Makaleyi reddet.
        
        Args:
            decision_notes: Karar notları
        """
        self.editor_decision = 'reject'
        self.editor_notes = decision_notes
        self.editor_decision_date = timezone.now()
    
    @transition(
        field=status,
        source=[Status.DRAFT, Status.SUBMITTED, Status.REVISION_REQUIRED],
        target=Status.WITHDRAWN
    )
    def withdraw(self):
        """Makaleyi geri çek (yazar tarafından)."""
        pass
    
    @transition(field=status, source=Status.ACCEPTED, target=Status.PUBLISHED)
    def publish(self):
        """Makaleyi yayınla."""
        self.published_at = timezone.now()
    
    # ============================================
    # YARDIMCI METODLAR
    # ============================================
    
    @property
    def is_editable(self):
        """Makale düzenlenebilir mi?"""
        return self.status in [self.Status.DRAFT, self.Status.REVISION_REQUIRED]
    
    @property
    def can_be_withdrawn(self):
        """Makale geri çekilebilir mi?"""
        return self.status in [
            self.Status.DRAFT,
            self.Status.SUBMITTED,
            self.Status.REVISION_REQUIRED
        ]
    
    @property
    def author_count(self):
        """Yazar sayısı."""
        return self.authors.count()
    
    @property
    def file_count(self):
        """Dosya sayısı."""
        return self.files.count()
    
    def get_corresponding_author(self):
        """Sorumlu yazarı döndür."""
        return self.authors.filter(is_corresponding=True).first()
    
    def get_status_history(self):
        """Durum geçmişini döndür."""
        return self.status_history.all().order_by('-created_at')


class Author(models.Model):
    """
    Yazar Modeli.
    
    Bir gönderime ait yazarları yönetir.
    Yazarlar sisteme kayıtlı kullanıcılar olabilir veya harici kişiler olabilir.
    
    İlişkiler:
    - Submission: Ait olduğu gönderim
    - User (opsiyonel): Sistemde kayıtlı kullanıcı
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
    # İLİŞKİLER
    # ============================================
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=_('Gönderim'),
        help_text=_('Bu yazarın ait olduğu gönderim')
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authorships',
        verbose_name=_('Kullanıcı'),
        help_text=_('Sistemde kayıtlı kullanıcı (varsa)')
    )
    
    # ============================================
    # YAZAR BİLGİLERİ
    # ============================================
    orcid_id = models.CharField(
        _('ORCID ID'),
        max_length=19,
        blank=True,
        help_text=_('Yazarın ORCID ID\'si')
    )
    
    given_name = models.CharField(
        _('Ad'),
        max_length=100,
        help_text=_('Yazarın adı')
    )
    
    family_name = models.CharField(
        _('Soyad'),
        max_length=100,
        help_text=_('Yazarın soyadı')
    )
    
    email = models.EmailField(
        _('Email'),
        help_text=_('Yazarın email adresi')
    )
    
    # ============================================
    # KURUM BİLGİLERİ
    # ============================================
    institution = models.CharField(
        _('Kurum'),
        max_length=255,
        help_text=_('Yazarın bağlı olduğu kurum')
    )
    
    department = models.CharField(
        _('Departman'),
        max_length=255,
        blank=True,
        help_text=_('Departman veya bölüm')
    )
    
    country = models.CharField(
        _('Ülke'),
        max_length=100,
        blank=True,
        help_text=_('Kurumun bulunduğu ülke')
    )
    
    city = models.CharField(
        _('Şehir'),
        max_length=100,
        blank=True,
        help_text=_('Kurumun bulunduğu şehir')
    )
    
    # ============================================
    # ROL VE SIRA
    # ============================================
    order = models.PositiveSmallIntegerField(
        _('Sıra'),
        default=1,
        help_text=_('Yazar listesindeki sıra (1 = birinci yazar)')
    )
    
    is_corresponding = models.BooleanField(
        _('Sorumlu Yazar'),
        default=False,
        help_text=_('Bu yazar sorumlu (corresponding) yazar mı?')
    )
    
    contribution = models.TextField(
        _('Katkı'),
        blank=True,
        help_text=_('Yazarın makaleye katkısı (CRediT taxonomy)')
    )
    
    # ============================================
    # ZAMAN DAMGALARI
    # ============================================
    created_at = models.DateTimeField(
        _('Oluşturulma Tarihi'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Güncellenme Tarihi'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Yazar')
        verbose_name_plural = _('Yazarlar')
        ordering = ['order']
        unique_together = [['submission', 'order']]
        indexes = [
            models.Index(fields=['submission', 'order']),
            models.Index(fields=['email']),
            models.Index(fields=['orcid_id']),
        ]
    
    def __str__(self):
        role = " (Sorumlu Yazar)" if self.is_corresponding else ""
        return f"{self.order}. {self.given_name} {self.family_name}{role}"
    
    @property
    def full_name(self):
        """Tam adı döndür."""
        return f"{self.given_name} {self.family_name}"
    
    @property
    def affiliation(self):
        """Kurum bilgisini formatla."""
        parts = [self.department, self.institution]
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        return ", ".join(filter(None, parts))
    
    def save(self, *args, **kwargs):
        """Kaydetmeden önce validasyonlar."""
        # Eğer bağlı kullanıcı varsa, bilgileri senkronize et
        if self.user and not self.orcid_id:
            self.orcid_id = self.user.orcid_id
        
        super().save(*args, **kwargs)
        
        # Sorumlu yazar değiştiğinde diğerlerini güncelle
        if self.is_corresponding:
            Author.objects.filter(
                submission=self.submission,
                is_corresponding=True
            ).exclude(pk=self.pk).update(is_corresponding=False)


class SubmissionStatusHistory(models.Model):
    """
    Gönderim Durum Geçmişi.
    Her durum değişikliği kaydedilir.
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='status_history',
        verbose_name=_('Gönderim')
    )
    
    from_status = models.CharField(
        _('Önceki Durum'),
        max_length=30,
        choices=Submission.Status.choices
    )
    
    to_status = models.CharField(
        _('Yeni Durum'),
        max_length=30,
        choices=Submission.Status.choices
    )
    
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Değiştiren')
    )
    
    notes = models.TextField(
        _('Notlar'),
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('Tarih'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Durum Geçmişi')
        verbose_name_plural = _('Durum Geçmişleri')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.submission.manuscript_id}: {self.from_status} → {self.to_status}"
