"""
TruEditor - User Model
======================
Custom user model with ORCID-based authentication.
No email/password registration - ORCID only.

Developer: Abdullah Dogan
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for ORCID-based authentication.
    """
    
    def create_user(self, orcid_id, email=None, **extra_fields):
        """
        Create a new user with ORCID ID.
        
        Args:
            orcid_id: ORCID identifier (required)
            email: Email address (optional, fetched from ORCID)
            **extra_fields: Additional fields
        
        Returns:
            User: Created user instance
        """
        if not orcid_id:
            raise ValueError(_('ORCID ID is required'))
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            orcid_id=orcid_id,
            email=email,
            **extra_fields
        )
        # ORCID users don't have passwords
        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, orcid_id, email=None, password=None, **extra_fields):
        """
        Create a superuser.
        Note: Password is required for admin panel access.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        
        user = self.create_user(orcid_id, email, **extra_fields)
        
        # Set password for admin access
        if password:
            user.set_password(password)
            user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    TruEditor Custom User Model.
    
    Authentication via ORCID ID only.
    No email/password registration.
    
    Field Groups:
    - ORCID information (required)
    - Personal information (from ORCID + manual)
    - Contact information
    - Academic information
    - Roles and permissions
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
    # ORCID INFORMATION (REQUIRED)
    # ============================================
    orcid_id = models.CharField(
        _('ORCID ID'),
        max_length=19,  # Format: 0000-0000-0000-0000
        unique=True,
        db_index=True,
        help_text=_('ORCID identifier (e.g., 0000-0002-1825-0097)')
    )
    
    orcid_access_token = models.TextField(
        _('ORCID Access Token'),
        blank=True,
        null=True,
        help_text=_('ORCID API access token')
    )
    
    orcid_refresh_token = models.TextField(
        _('ORCID Refresh Token'),
        blank=True,
        null=True,
        help_text=_('ORCID token refresh token')
    )
    
    orcid_token_expires = models.DateTimeField(
        _('Token Expiry'),
        null=True,
        blank=True,
        help_text=_('When the ORCID access token expires')
    )
    
    orcid_data = models.JSONField(
        _('ORCID Profile Data'),
        default=dict,
        blank=True,
        help_text=_('Raw profile data from ORCID API')
    )
    
    last_orcid_sync = models.DateTimeField(
        _('Last ORCID Sync'),
        null=True,
        blank=True,
        help_text=_('When the ORCID profile was last synchronized')
    )
    
    # ============================================
    # PERSONAL INFORMATION
    # ============================================
    email = models.EmailField(
        _('Email Address'),
        blank=True,
        null=True,
        db_index=True,
        help_text=_('Contact email address')
    )
    
    full_name = models.CharField(
        _('Full Name'),
        max_length=255,
        blank=True,
        help_text=_('Full name')
    )
    
    given_name = models.CharField(
        _('Given Name'),
        max_length=100,
        blank=True,
        help_text=_('First name')
    )
    
    family_name = models.CharField(
        _('Family Name'),
        max_length=100,
        blank=True,
        help_text=_('Last name')
    )
    
    # ============================================
    # CONTACT INFORMATION
    # ============================================
    phone = models.CharField(
        _('Phone'),
        max_length=20,
        blank=True,
        help_text=_('Contact phone number')
    )
    
    country = models.CharField(
        _('Country'),
        max_length=100,
        blank=True,
        help_text=_('Country')
    )
    
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True,
        help_text=_('City')
    )
    
    address = models.TextField(
        _('Address'),
        blank=True,
        help_text=_('Mailing address')
    )
    
    # ============================================
    # ACADEMIC INFORMATION
    # ============================================
    title = models.CharField(
        _('Title'),
        max_length=50,
        blank=True,
        choices=[
            ('', _('Select')),
            ('prof', _('Professor')),
            ('assoc_prof', _('Associate Professor')),
            ('asst_prof', _('Assistant Professor')),
            ('dr', _('Doctor')),
            ('lecturer', _('Lecturer')),
            ('researcher', _('Researcher')),
            ('phd_student', _('PhD Student')),
            ('msc_student', _('MSc Student')),
            ('other', _('Other')),
        ],
        help_text=_('Academic title')
    )
    
    institution = models.CharField(
        _('Institution'),
        max_length=255,
        blank=True,
        help_text=_('Affiliated institution')
    )
    
    department = models.CharField(
        _('Department'),
        max_length=255,
        blank=True,
        help_text=_('Department or division')
    )
    
    expertise_areas = models.JSONField(
        _('Expertise Areas'),
        default=list,
        blank=True,
        help_text=_('List of expertise areas')
    )
    
    bio = models.TextField(
        _('Biography'),
        blank=True,
        max_length=1000,
        help_text=_('Short biography (max 1000 characters)')
    )
    
    website = models.URLField(
        _('Website'),
        blank=True,
        help_text=_('Personal or institutional website')
    )
    
    # ============================================
    # ROLES AND PERMISSIONS
    # ============================================
    is_reviewer = models.BooleanField(
        _('Is Reviewer'),
        default=False,
        help_text=_('Can the user serve as a reviewer?')
    )
    
    is_editor = models.BooleanField(
        _('Is Editor'),
        default=False,
        help_text=_('Can the user serve as an editor?')
    )
    
    is_chief_editor = models.BooleanField(
        _('Is Chief Editor'),
        default=False,
        help_text=_('Is the user a chief editor?')
    )
    
    reviewer_interests = models.JSONField(
        _('Reviewer Interests'),
        default=list,
        blank=True,
        help_text=_('Areas of interest for reviewing')
    )
    
    # ============================================
    # DJANGO STANDARD FIELDS
    # ============================================
    is_staff = models.BooleanField(
        _('Staff Status'),
        default=False,
        help_text=_('Can the user access the admin panel?')
    )
    
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        db_index=True,
        help_text=_('Is the user account active?')
    )
    
    email_verified = models.BooleanField(
        _('Email Verified'),
        default=False,
        help_text=_('Has the email address been verified?')
    )
    
    profile_completed = models.BooleanField(
        _('Profile Completed'),
        default=False,
        help_text=_('Has the user completed their profile?')
    )
    
    # ============================================
    # TIMESTAMPS
    # ============================================
    date_joined = models.DateTimeField(
        _('Date Joined'),
        default=timezone.now
    )
    
    last_login = models.DateTimeField(
        _('Last Login'),
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True
    )
    
    # ============================================
    # MANAGER
    # ============================================
    objects = UserManager()
    
    # Authentication settings
    USERNAME_FIELD = 'orcid_id'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['orcid_id']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_reviewer']),
            models.Index(fields=['is_editor']),
        ]
    
    def __str__(self):
        """String representation of the user."""
        if self.full_name:
            return f"{self.full_name} ({self.orcid_id})"
        return self.orcid_id
    
    def get_full_name(self):
        """Return the full name."""
        if self.full_name:
            return self.full_name
        if self.given_name or self.family_name:
            return f"{self.given_name} {self.family_name}".strip()
        return self.orcid_id
    
    def get_short_name(self):
        """Return the short name (given name)."""
        return self.given_name or self.orcid_id
    
    @property
    def orcid_url(self):
        """Return the ORCID profile URL."""
        return f"https://orcid.org/{self.orcid_id}"
    
    @property
    def display_name(self):
        """Return the display name with title."""
        if self.title and self.full_name:
            return f"{self.get_title_display()} {self.full_name}"
        return self.get_full_name()
    
    def check_profile_completion(self):
        """
        Check if the profile is complete.
        Returns True if all required fields are filled.
        """
        required_fields = ['full_name', 'email', 'institution']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True
    
    def update_profile_completion(self):
        """Update the profile completion status."""
        self.profile_completed = self.check_profile_completion()
        self.save(update_fields=['profile_completed', 'updated_at'])
    
    def update_from_orcid(self, orcid_data: dict):
        """
        Update user profile from ORCID API data.
        
        Args:
            orcid_data: Profile data returned from ORCID API
        """
        # Person information
        person = orcid_data.get('person', {})
        name = person.get('name', {})
        
        # Name
        if name.get('given-names'):
            self.given_name = name['given-names'].get('value', '')
        if name.get('family-name'):
            self.family_name = name['family-name'].get('value', '')
        
        self.full_name = f"{self.given_name} {self.family_name}".strip()
        
        # Email
        emails = person.get('emails', {}).get('email', [])
        if emails and not self.email:
            # Prefer primary or verified email
            for email in emails:
                if email.get('primary') or email.get('verified'):
                    self.email = email.get('email')
                    break
            if not self.email and emails:
                self.email = emails[0].get('email')
        
        # Country
        addresses = person.get('addresses', {}).get('address', [])
        if addresses and not self.country:
            self.country = addresses[0].get('country', {}).get('value', '')
        
        # Institution (from activities)
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
        
        # Biography
        biography = person.get('biography', {})
        if biography and not self.bio:
            self.bio = biography.get('content', '')[:1000]
        
        # Website
        researcher_urls = person.get('researcher-urls', {}).get('researcher-url', [])
        if researcher_urls and not self.website:
            self.website = researcher_urls[0].get('url', {}).get('value', '')
        
        # Store raw data
        self.orcid_data = orcid_data
        self.last_orcid_sync = timezone.now()
        
        # Update profile completion status
        self.profile_completed = self.check_profile_completion()
        
        self.save()
