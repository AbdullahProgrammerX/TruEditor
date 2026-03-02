from django.contrib import admin
from .models import Submission, Author, SubmissionStatusHistory


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('manuscript_id', 'title_short', 'submitter_email', 'status', 'article_type', 'revision_number', 'created_at')
    list_filter = ('status', 'article_type', 'language')
    search_fields = ('manuscript_id', 'title', 'submitter__email')
    readonly_fields = ('id', 'manuscript_id', 'created_at', 'updated_at', 'submitted_at', 'accepted_at', 'published_at', 'revision_submitted_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Status', {
            'fields': ('id', 'manuscript_id', 'status', 'submitter')
        }),
        ('Manuscript', {
            'fields': ('title', 'title_en', 'abstract', 'abstract_en', 'keywords', 'keywords_en', 'article_type', 'language')
        }),
        ('Revision', {
            'fields': ('revision_number', 'revision_notes', 'revision_deadline', 'revision_response', 'revision_submitted_at'),
            'classes': ('collapse',),
        }),
        ('Editor', {
            'fields': ('assigned_editor', 'editor_notes', 'editor_decision', 'editor_decision_date'),
            'classes': ('collapse',),
        }),
        ('Details', {
            'fields': ('cover_letter', 'ethics_statement', 'ethics_approval_number', 'conflict_of_interest', 'funding_statement'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'submitted_at', 'accepted_at', 'published_at'),
        }),
    )

    def title_short(self, obj):
        return (obj.title or 'Untitled')[:50]
    title_short.short_description = 'Title'

    def submitter_email(self, obj):
        return obj.submitter.email if obj.submitter else '—'
    submitter_email.short_description = 'Submitter'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'submission_id_short', 'is_corresponding', 'order')
    list_filter = ('is_corresponding',)
    search_fields = ('first_name', 'last_name', 'email')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def submission_id_short(self, obj):
        return obj.submission.manuscript_id or str(obj.submission_id)[:8]
    submission_id_short.short_description = 'Submission'


@admin.register(SubmissionStatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('submission_manuscript', 'from_status', 'to_status', 'changed_by_name', 'created_at')
    list_filter = ('to_status',)
    readonly_fields = ('submission', 'from_status', 'to_status', 'changed_by', 'notes', 'created_at')

    def submission_manuscript(self, obj):
        return obj.submission.manuscript_id or str(obj.submission_id)[:8]
    submission_manuscript.short_description = 'Submission'

    def changed_by_name(self, obj):
        return obj.changed_by.email if obj.changed_by else 'System'
    changed_by_name.short_description = 'Changed By'
