"""
TruEditor - Submission Models
=============================
Database models for manuscript submissions.
FSM (Finite State Machine) for state management.

Developer: Abdullah Dogan
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
    Manuscript Submission Model.
    
    Manages the entire lifecycle of a manuscript submission:
    - draft → submitted → under_review → revision_required → accepted/rejected
    
    Relations:
    - User (submitter): User who submitted the manuscript
    - Author: Authors (ordered list)
    - ManuscriptFile: Uploaded files
    """
    
    # ============================================
    # STATUS CHOICES
    # ============================================
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SUBMITTED = 'submitted', _('Submitted')
        UNDER_REVIEW = 'under_review', _('Under Review')
        REVISION_REQUIRED = 'revision_required', _('Revision Required')
        REVISION_SUBMITTED = 'revision_submitted', _('Revision Submitted')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        WITHDRAWN = 'withdrawn', _('Withdrawn')
        PUBLISHED = 'published', _('Published')
    
    # ============================================
    # ARTICLE TYPES
    # ============================================
    class ArticleType(models.TextChoices):
        RESEARCH = 'research', _('Research Article')
        REVIEW = 'review', _('Review Article')
        CASE_REPORT = 'case_report', _('Case Report')
        SHORT_COMM = 'short_communication', _('Short Communication')
        LETTER = 'letter', _('Letter to the Editor')
        EDITORIAL = 'editorial', _('Editorial')
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
    # SUBMISSION INFORMATION
    # ============================================
    manuscript_id = models.CharField(
        _('Manuscript ID'),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Auto-generated manuscript number (e.g., TRU-2026-0001)')
    )
    
    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='submissions',
        verbose_name=_('Submitter'),
        help_text=_('User who submitted the manuscript')
    )
    
    # ============================================
    # STATUS (FSM)
    # ============================================
    status = FSMField(
        _('Status'),
        default=Status.DRAFT,
        choices=Status.choices,
        db_index=True,
        protected=True,  # Can only be changed via transitions
        help_text=_('Current status of the manuscript')
    )
    
    # ============================================
    # MANUSCRIPT INFORMATION
    # ============================================
    title = models.CharField(
        _('Title'),
        max_length=500,
        help_text=_('Title of the manuscript')
    )
    
    title_en = models.CharField(
        _('English Title'),
        max_length=500,
        blank=True,
        help_text=_('English title of the manuscript (optional)')
    )
    
    abstract = models.TextField(
        _('Abstract'),
        max_length=5000,
        help_text=_('Abstract of the manuscript (max 5000 characters)')
    )
    
    abstract_en = models.TextField(
        _('English Abstract'),
        max_length=5000,
        blank=True,
        help_text=_('English abstract (optional)')
    )
    
    keywords = models.JSONField(
        _('Keywords'),
        default=list,
        help_text=_('List of keywords')
    )
    
    keywords_en = models.JSONField(
        _('English Keywords'),
        default=list,
        blank=True,
        help_text=_('English keywords')
    )
    
    article_type = models.CharField(
        _('Article Type'),
        max_length=30,
        choices=ArticleType.choices,
        default=ArticleType.RESEARCH,
        help_text=_('Type of the article')
    )
    
    language = models.CharField(
        _('Language'),
        max_length=5,
        default='en',
        choices=[
            ('en', _('English')),
            ('tr', _('Turkish')),
        ],
        help_text=_('Language of the manuscript')
    )
    
    # ============================================
    # COVER LETTER AND ETHICS
    # ============================================
    cover_letter = models.TextField(
        _('Cover Letter'),
        blank=True,
        help_text=_('Cover letter to the editor')
    )
    
    ethics_statement = models.TextField(
        _('Ethics Statement'),
        blank=True,
        help_text=_('Ethics approval and statement')
    )
    
    ethics_approval_number = models.CharField(
        _('Ethics Approval Number'),
        max_length=100,
        blank=True,
        help_text=_('Ethics committee approval number (if applicable)')
    )
    
    conflict_of_interest = models.TextField(
        _('Conflict of Interest Statement'),
        blank=True,
        help_text=_('Conflict of interest declaration')
    )
    
    funding_statement = models.TextField(
        _('Funding Statement'),
        blank=True,
        help_text=_('Research funding information')
    )
    
    # ============================================
    # WIZARD PROGRESS
    # ============================================
    wizard_step = models.PositiveSmallIntegerField(
        _('Wizard Step'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        help_text=_('Current step in the submission wizard (1-6)')
    )
    
    wizard_data = models.JSONField(
        _('Wizard Data'),
        default=dict,
        blank=True,
        help_text=_('Temporary data collected from wizard steps')
    )
    
    # ============================================
    # REVISION INFORMATION
    # ============================================
    revision_number = models.PositiveSmallIntegerField(
        _('Revision Number'),
        default=0,
        help_text=_('Current revision number')
    )
    
    revision_notes = models.TextField(
        _('Revision Notes'),
        blank=True,
        help_text=_('Editor revision request notes')
    )
    
    revision_deadline = models.DateTimeField(
        _('Revision Deadline'),
        null=True,
        blank=True,
        help_text=_('Deadline for revision submission')
    )
    
    # ============================================
    # EDITOR ASSIGNMENT
    # ============================================
    assigned_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='editor_submissions',
        verbose_name=_('Assigned Editor'),
        help_text=_('Editor handling this manuscript')
    )
    
    editor_notes = models.TextField(
        _('Editor Notes'),
        blank=True,
        help_text=_('Internal notes from the editor')
    )
    
    editor_decision = models.CharField(
        _('Editor Decision'),
        max_length=50,
        blank=True,
        choices=[
            ('accept', _('Accept')),
            ('minor_revision', _('Minor Revision')),
            ('major_revision', _('Major Revision')),
            ('reject', _('Reject')),
        ],
        help_text=_('Final decision by the editor')
    )
    
    editor_decision_date = models.DateTimeField(
        _('Decision Date'),
        null=True,
        blank=True,
        help_text=_('Date when the decision was made')
    )
    
    # ============================================
    # TIMESTAMPS
    # ============================================
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True
    )
    
    submitted_at = models.DateTimeField(
        _('Submitted At'),
        null=True,
        blank=True,
        help_text=_('Date when the manuscript was first submitted')
    )
    
    accepted_at = models.DateTimeField(
        _('Accepted At'),
        null=True,
        blank=True,
        help_text=_('Date when the manuscript was accepted')
    )
    
    published_at = models.DateTimeField(
        _('Published At'),
        null=True,
        blank=True,
        help_text=_('Date when the manuscript was published')
    )
    
    class Meta:
        verbose_name = _('Submission')
        verbose_name_plural = _('Submissions')
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
        """Generate manuscript_id before saving if submitted."""
        if not self.manuscript_id and self.status != self.Status.DRAFT:
            self.manuscript_id = self.generate_manuscript_id()
        super().save(*args, **kwargs)
    
    def generate_manuscript_id(self):
        """
        Generate a unique manuscript ID.
        Format: TRU-YYYY-NNNN
        """
        year = timezone.now().year
        prefix = f"TRU-{year}-"
        
        # Find the last number for this year
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
    # FSM STATE TRANSITIONS
    # ============================================
    
    @transition(field=status, source=Status.DRAFT, target=Status.SUBMITTED)
    def submit(self):
        """
        Submit the draft.
        Validations should be done before the transition.
        """
        self.submitted_at = timezone.now()
        self.manuscript_id = self.generate_manuscript_id()
    
    @transition(field=status, source=Status.SUBMITTED, target=Status.UNDER_REVIEW)
    def start_review(self, editor):
        """
        Start the review process.
        
        Args:
            editor: Assigned editor
        """
        self.assigned_editor = editor
    
    @transition(
        field=status,
        source=[Status.UNDER_REVIEW, Status.REVISION_SUBMITTED],
        target=Status.REVISION_REQUIRED
    )
    def request_revision(self, notes, deadline_days=30):
        """
        Request revision.
        
        Args:
            notes: Revision notes
            deadline_days: Number of days for revision
        """
        self.revision_notes = notes
        self.revision_deadline = timezone.now() + timezone.timedelta(days=deadline_days)
        self.revision_number += 1
    
    @transition(field=status, source=Status.REVISION_REQUIRED, target=Status.REVISION_SUBMITTED)
    def submit_revision(self):
        """Submit the revision."""
        pass
    
    @transition(
        field=status,
        source=[Status.UNDER_REVIEW, Status.REVISION_SUBMITTED],
        target=Status.ACCEPTED
    )
    def accept(self, decision_notes=''):
        """
        Accept the manuscript.
        
        Args:
            decision_notes: Decision notes
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
        Reject the manuscript.
        
        Args:
            decision_notes: Decision notes
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
        """Withdraw the manuscript (by author)."""
        pass
    
    @transition(field=status, source=Status.ACCEPTED, target=Status.PUBLISHED)
    def publish(self):
        """Publish the manuscript."""
        self.published_at = timezone.now()
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    @property
    def is_editable(self):
        """Check if the manuscript can be edited."""
        return self.status in [self.Status.DRAFT, self.Status.REVISION_REQUIRED]
    
    @property
    def can_be_withdrawn(self):
        """Check if the manuscript can be withdrawn."""
        return self.status in [
            self.Status.DRAFT,
            self.Status.SUBMITTED,
            self.Status.REVISION_REQUIRED
        ]
    
    @property
    def author_count(self):
        """Return the number of authors."""
        return self.authors.count()
    
    @property
    def file_count(self):
        """Return the number of files."""
        return self.files.count()
    
    def get_corresponding_author(self):
        """Return the corresponding author."""
        return self.authors.filter(is_corresponding=True).first()
    
    def get_status_history(self):
        """Return the status history."""
        return self.status_history.all().order_by('-created_at')


class Author(models.Model):
    """
    Author Model.
    
    Manages authors for a submission.
    Authors can be registered users or external contributors.
    
    Relations:
    - Submission: Parent submission
    - User (optional): Registered user in the system
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
    # RELATIONS
    # ============================================
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name=_('Submission'),
        help_text=_('Submission this author belongs to')
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authorships',
        verbose_name=_('User'),
        help_text=_('Registered user in the system (if any)')
    )
    
    # ============================================
    # AUTHOR INFORMATION
    # ============================================
    orcid_id = models.CharField(
        _('ORCID ID'),
        max_length=19,
        blank=True,
        help_text=_('Author\'s ORCID ID')
    )
    
    given_name = models.CharField(
        _('Given Name'),
        max_length=100,
        help_text=_('Author\'s first name')
    )
    
    family_name = models.CharField(
        _('Family Name'),
        max_length=100,
        help_text=_('Author\'s last name')
    )
    
    email = models.EmailField(
        _('Email'),
        help_text=_('Author\'s email address')
    )
    
    # ============================================
    # AFFILIATION INFORMATION
    # ============================================
    institution = models.CharField(
        _('Institution'),
        max_length=255,
        help_text=_('Author\'s affiliated institution')
    )
    
    department = models.CharField(
        _('Department'),
        max_length=255,
        blank=True,
        help_text=_('Department or division')
    )
    
    country = models.CharField(
        _('Country'),
        max_length=100,
        blank=True,
        help_text=_('Country of the institution')
    )
    
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True,
        help_text=_('City of the institution')
    )
    
    # ============================================
    # ROLE AND ORDER
    # ============================================
    order = models.PositiveSmallIntegerField(
        _('Order'),
        default=1,
        help_text=_('Order in the author list (1 = first author)')
    )
    
    is_corresponding = models.BooleanField(
        _('Corresponding Author'),
        default=False,
        help_text=_('Is this the corresponding author?')
    )
    
    contribution = models.TextField(
        _('Contribution'),
        blank=True,
        help_text=_('Author\'s contribution to the manuscript (CRediT taxonomy)')
    )
    
    # ============================================
    # TIMESTAMPS
    # ============================================
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['order']
        unique_together = [['submission', 'order']]
        indexes = [
            models.Index(fields=['submission', 'order']),
            models.Index(fields=['email']),
            models.Index(fields=['orcid_id']),
        ]
    
    def __str__(self):
        role = " (Corresponding)" if self.is_corresponding else ""
        return f"{self.order}. {self.given_name} {self.family_name}{role}"
    
    @property
    def full_name(self):
        """Return the full name."""
        return f"{self.given_name} {self.family_name}"
    
    @property
    def affiliation(self):
        """Format the affiliation string."""
        parts = [self.department, self.institution]
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        return ", ".join(filter(None, parts))
    
    def save(self, *args, **kwargs):
        """Perform validations before saving."""
        # Sync ORCID ID from linked user
        if self.user and not self.orcid_id:
            self.orcid_id = self.user.orcid_id
        
        super().save(*args, **kwargs)
        
        # Ensure only one corresponding author
        if self.is_corresponding:
            Author.objects.filter(
                submission=self.submission,
                is_corresponding=True
            ).exclude(pk=self.pk).update(is_corresponding=False)


class SubmissionStatusHistory(models.Model):
    """
    Submission Status History.
    Records every status change for audit purposes.
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
        verbose_name=_('Submission')
    )
    
    from_status = models.CharField(
        _('From Status'),
        max_length=30,
        choices=Submission.Status.choices
    )
    
    to_status = models.CharField(
        _('To Status'),
        max_length=30,
        choices=Submission.Status.choices
    )
    
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Changed By')
    )
    
    notes = models.TextField(
        _('Notes'),
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Status History')
        verbose_name_plural = _('Status Histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.submission.manuscript_id}: {self.from_status} → {self.to_status}"
