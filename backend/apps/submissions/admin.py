from django.contrib import admin
from django.utils import timezone
from .models import Submission, Author, SubmissionStatusHistory


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('manuscript_id', 'title_short', 'submitter_email', 'status', 'article_type', 'revision_number', 'created_at')
    list_filter = ('status', 'article_type', 'language')
    search_fields = ('manuscript_id', 'title', 'submitter__email')
    readonly_fields = ('id', 'manuscript_id', 'status', 'created_at', 'updated_at', 'submitted_at', 'accepted_at', 'published_at', 'revision_submitted_at')
    ordering = ('-created_at',)
    actions = ['action_request_revision', 'action_accept', 'action_reject', 'action_start_review']

    fieldsets = (
        ('Status', {
            'fields': ('id', 'manuscript_id', 'status', 'submitter')
        }),
        ('Manuscript', {
            'fields': ('title', 'title_en', 'abstract', 'abstract_en', 'keywords', 'keywords_en', 'article_type', 'language')
        }),
        ('Revision', {
            'fields': ('revision_number', 'revision_notes', 'revision_deadline', 'revision_response', 'revision_submitted_at'),
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

    @admin.action(description='Request Revision (submitted/under_review → revision_required)')
    def action_request_revision(self, request, queryset):
        count = 0
        for sub in queryset:
            try:
                old_status = sub.status
                notes = sub.revision_notes or 'Please revise your manuscript.'
                sub.request_revision(notes=notes, deadline_days=30)
                sub.save()
                SubmissionStatusHistory.objects.create(
                    submission=sub, from_status=old_status,
                    to_status=sub.status, changed_by=request.user,
                    notes='Revision requested via admin',
                )
                count += 1
            except Exception as e:
                self.message_user(request, f'Error on {sub.manuscript_id}: {e}', level='error')
        self.message_user(request, f'{count} submission(s) set to revision_required.')

    @admin.action(description='Start Review (submitted → under_review)')
    def action_start_review(self, request, queryset):
        count = 0
        for sub in queryset:
            try:
                old_status = sub.status
                sub.start_review()
                sub.save()
                SubmissionStatusHistory.objects.create(
                    submission=sub, from_status=old_status,
                    to_status=sub.status, changed_by=request.user,
                    notes='Review started via admin',
                )
                count += 1
            except Exception as e:
                self.message_user(request, f'Error on {sub.manuscript_id}: {e}', level='error')
        self.message_user(request, f'{count} submission(s) set to under_review.')

    @admin.action(description='Accept (under_review/revision_submitted → accepted)')
    def action_accept(self, request, queryset):
        count = 0
        for sub in queryset:
            try:
                old_status = sub.status
                sub.accept()
                sub.save()
                SubmissionStatusHistory.objects.create(
                    submission=sub, from_status=old_status,
                    to_status=sub.status, changed_by=request.user,
                    notes='Accepted via admin',
                )
                count += 1
            except Exception as e:
                self.message_user(request, f'Error on {sub.manuscript_id}: {e}', level='error')
        self.message_user(request, f'{count} submission(s) accepted.')

    @admin.action(description='Reject (submitted/under_review → rejected)')
    def action_reject(self, request, queryset):
        count = 0
        for sub in queryset:
            try:
                old_status = sub.status
                sub.reject()
                sub.save()
                SubmissionStatusHistory.objects.create(
                    submission=sub, from_status=old_status,
                    to_status=sub.status, changed_by=request.user,
                    notes='Rejected via admin',
                )
                count += 1
            except Exception as e:
                self.message_user(request, f'Error on {sub.manuscript_id}: {e}', level='error')
        self.message_user(request, f'{count} submission(s) rejected.')


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
