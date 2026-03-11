"""
TruEditor - Submission Views
=============================
API views for manuscript submissions (Author Module).

Developer: Abdullah Dogan
"""

import logging
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from .models import Submission, Author, SubmissionStatusHistory, Correspondence
from .serializers import (
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionCreateSerializer,
    SubmissionUpdateSerializer,
    AuthorCreateSerializer,
    SubmissionSubmitSerializer,
    CorrespondenceSerializer,
    CorrespondenceCreateSerializer,
)
from .permissions import IsOwnerOrReadOnly, CanEditSubmission, CanDeleteSubmission
from apps.common.response import (
    success_response,
    error_response,
    created_response,
    validation_error_response,
    not_found_response,
    forbidden_response,
)

logger = logging.getLogger(__name__)


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing submissions.
    
    Actions:
    - list: Get user's submissions (filtered by status)
    - create: Create new DRAFT submission
    - retrieve: Get submission details
    - update/partial_update: Update submission (only DRAFT/REVISION_REQUIRED)
    - destroy: Delete submission (only DRAFT)
    - build_pdf: Trigger PDF generation
    - approve: Author approval
    - submit: Final submission
    """
    
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, CanEditSubmission, CanDeleteSubmission]
    
    def get_queryset(self):
        """
        Return submissions for the current user.
        Optimized with select_related and prefetch_related.
        """
        queryset = Submission.objects.filter(
            submitter=self.request.user
        ).select_related(
            'submitter',
            'assigned_editor'
        ).prefetch_related(
            'authors',
            'files',
            'status_history',
            'status_history__changed_by',
        ).order_by('-created_at')
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return SubmissionListSerializer
        elif self.action == 'create':
            return SubmissionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SubmissionUpdateSerializer
        return SubmissionDetailSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List user's submissions.
        
        Query params:
        - status: Filter by status (optional)
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return success_response(
                data={
                    'count': self.paginator.page.paginator.count,
                    'next': self.paginator.get_next_link(),
                    'previous': self.paginator.get_previous_link(),
                    'results': serializer.data,
                },
                message=_('Submissions retrieved successfully')
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data={
                'count': len(serializer.data),
                'next': None,
                'previous': None,
                'results': serializer.data,
            },
            message=_('Submissions retrieved successfully')
        )
    
    def create(self, request, *args, **kwargs):
        """
        Create a new DRAFT submission.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        submission = serializer.save()
        
        return created_response(
            data=SubmissionDetailSerializer(submission).data,
            message=_('Submission created successfully')
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get submission details.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return success_response(
            data=serializer.data,
            message=_('Submission retrieved successfully')
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update submission.
        Only allowed for DRAFT or REVISION_REQUIRED status.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if editable
        if not instance.is_editable:
            return forbidden_response(
                _('This submission cannot be edited in its current status.')
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return success_response(
            data=SubmissionDetailSerializer(instance).data,
            message=_('Submission updated successfully')
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete submission.
        Only allowed for DRAFT status.
        """
        instance = self.get_object()
        
        if instance.status != Submission.Status.DRAFT:
            return forbidden_response(
                _('Only draft submissions can be deleted.')
            )
        
        self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def build_pdf(self, request, pk=None):
        """
        Generate submission PDF synchronously.
        Returns the generated file info with a download URL.
        """
        from .pdf_service import generate_submission_pdf
        from apps.files.services import FileService

        submission = self.get_object()

        try:
            manuscript_file = generate_submission_pdf(submission, user=request.user)
            download_url = FileService.get_presigned_url(manuscript_file)

            return success_response(
                data={
                    'file_id': str(manuscript_file.id),
                    'filename': manuscript_file.original_filename,
                    'file_size': manuscript_file.file_size,
                    'download_url': download_url,
                },
                message=_('PDF generated successfully')
            )
        except Exception as e:
            logger.error(f"PDF generation failed for {submission.id}: {e}")
            return error_response(
                message=_('PDF generation failed. Please try again later.'),
                code='PDF_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Author approval step.
        Marks submission as ready for final submission.
        """
        submission = self.get_object()
        
        if submission.status != Submission.Status.DRAFT:
            return validation_error_response(
                _('Only draft submissions can be approved.')
            )
        
        # Validation: Check required fields
        if not submission.title:
            return validation_error_response(
                _('Title is required.')
            )
        
        if not submission.abstract:
            return validation_error_response(
                _('Abstract is required.')
            )
        
        if submission.authors.count() == 0:
            return validation_error_response(
                _('At least one author is required.')
            )
        
        if submission.files.filter(is_active=True).count() == 0:
            return validation_error_response(
                _('At least one file is required.')
            )
        
        # Approval is just a validation step
        # No status change, just return success
        return success_response(
            data=SubmissionDetailSerializer(submission).data,
            message=_('Submission approved and ready for final submission')
        )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Final submission.
        Transitions status from DRAFT to SUBMITTED.
        """
        submission = self.get_object()
        
        if submission.status != Submission.Status.DRAFT:
            return validation_error_response(
                _('Only draft submissions can be submitted.')
            )
        
        # Validate submission completeness
        serializer = SubmissionSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Final validations
        if not submission.title:
            return validation_error_response(
                _('Title is required.')
            )
        
        if not submission.abstract:
            return validation_error_response(
                _('Abstract is required.')
            )
        
        if submission.authors.count() == 0:
            return validation_error_response(
                _('At least one author is required.')
            )
        
        if submission.files.filter(is_active=True).count() == 0:
            return validation_error_response(
                _('At least one file is required.')
            )
        
        # Check for corresponding author
        if not submission.authors.filter(is_corresponding=True).exists():
            return validation_error_response(
                _('At least one corresponding author is required.')
            )
        
        # Perform FSM transition
        try:
            old_status = submission.status
            submission.submit()
            submission.save()

            SubmissionStatusHistory.objects.create(
                submission=submission,
                from_status=old_status,
                to_status=submission.status,
                changed_by=request.user,
                notes=_('Manuscript submitted by author'),
            )
            
            logger.info(
                f"Submission {submission.manuscript_id} submitted by {request.user.email}"
            )

            # Send confirmation email (non-blocking)
            try:
                from apps.notifications.email_service import send_submission_confirmation
                send_submission_confirmation(submission)
            except Exception as email_err:
                logger.warning(f"Submission email failed: {email_err}")
            
            return success_response(
                data=SubmissionDetailSerializer(submission).data,
                message=_('Submission submitted successfully')
            )
        except Exception as e:
            logger.error(f"Error submitting submission: {str(e)}")
            return error_response(
                message=_('Failed to submit submission'),
                code='SUBMISSION_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def task_status(self, request, pk=None):
        """
        Get PDF generation task status.
        
        Query params:
        - task_id: Celery task ID
        """
        task_id = request.query_params.get('task_id')
        
        if not task_id:
            return validation_error_response(
                _('task_id parameter is required.')
            )
        
        # TODO: Implement in Phase 7
        # from celery.result import AsyncResult
        # result = AsyncResult(task_id)
        # return success_response(data={'status': result.status, 'result': result.result})
        
        return success_response(
            data={'status': 'pending', 'message': 'Task status will be implemented in Phase 7'},
            message=_('Task status retrieved')
        )
    
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        """Withdraw a submission (by author)."""
        submission = self.get_object()

        if not submission.can_be_withdrawn:
            return validation_error_response(
                _('This submission cannot be withdrawn in its current status.')
            )

        try:
            old_status = submission.status
            submission.withdraw()
            submission.save()

            SubmissionStatusHistory.objects.create(
                submission=submission,
                from_status=old_status,
                to_status=submission.status,
                changed_by=request.user,
                notes=_('Manuscript withdrawn by author'),
            )

            logger.info(
                f"Submission {submission.manuscript_id or submission.id} withdrawn by {request.user.email}"
            )

            # Send withdrawal confirmation email (non-blocking)
            try:
                from apps.notifications.email_service import send_withdrawal_confirmation
                send_withdrawal_confirmation(submission)
            except Exception as email_err:
                logger.warning(f"Withdrawal email failed: {email_err}")

            return success_response(
                data=SubmissionDetailSerializer(submission).data,
                message=_('Submission withdrawn successfully')
            )
        except Exception as e:
            logger.error(f"Error withdrawing submission: {str(e)}")
            return error_response(
                message=_('Failed to withdraw submission'),
                code='WITHDRAW_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def submit_revision(self, request, pk=None):
        """
        Submit a revision for a manuscript in revision_required status.
        Expects: { revision_response: "..." }
        """
        submission = self.get_object()

        if submission.status != Submission.Status.REVISION_REQUIRED:
            return validation_error_response(
                _('This submission is not awaiting a revision.')
            )

        revision_response = request.data.get('revision_response', '').strip()
        if not revision_response:
            return validation_error_response(
                _('A response to reviewer comments is required.')
            )

        try:
            old_status = submission.status
            submission.revision_response = revision_response
            submission.submit_revision()
            submission.save()

            SubmissionStatusHistory.objects.create(
                submission=submission,
                from_status=old_status,
                to_status=submission.status,
                changed_by=request.user,
                notes=_('Revision submitted by author'),
            )

            logger.info(
                f"Revision #{submission.revision_number} submitted for {submission.manuscript_id}"
            )

            try:
                from apps.notifications.email_service import send_status_change
                send_status_change(
                    submission, old_status, submission.status,
                    notes=f'Revision #{submission.revision_number} submitted'
                )
            except Exception as email_err:
                logger.warning(f"Revision email failed: {email_err}")

            return success_response(
                data=SubmissionDetailSerializer(submission).data,
                message=_('Revision submitted successfully')
            )
        except Exception as e:
            logger.error(f"Error submitting revision: {str(e)}")
            return error_response(
                message=_('Failed to submit revision'),
                code='REVISION_ERROR',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get', 'post'])
    def authors(self, request, pk=None):
        """
        Manage authors for a submission.
        
        GET: List authors
        POST: Add new author
        """
        submission = self.get_object()
        
        if request.method == 'GET':
            authors = submission.authors.all().order_by('order')
            serializer = AuthorCreateSerializer(authors, many=True)
            
            return success_response(
                data=serializer.data,
                message=_('Authors retrieved successfully')
            )
        
        elif request.method == 'POST':
            serializer = AuthorCreateSerializer(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            author = serializer.save(submission=submission)
            
            return created_response(
                data=AuthorCreateSerializer(author).data,
                message=_('Author added successfully')
            )
    
    @action(detail=True, methods=['put', 'delete'], url_path='authors/(?P<author_id>[^/.]+)')
    def author_detail(self, request, pk=None, author_id=None):
        """
        Update or delete an author.
        
        PUT: Update author
        DELETE: Remove author
        """
        submission = self.get_object()
        
        try:
            author = submission.authors.get(id=author_id)
        except Author.DoesNotExist:
            return not_found_response(
                _('Author not found.')
            )
        
        if request.method == 'PUT':
            serializer = AuthorCreateSerializer(
                author,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            author = serializer.save()
            
            return success_response(
                data=AuthorCreateSerializer(author).data,
                message=_('Author updated successfully')
            )
        
        elif request.method == 'DELETE':
            author.delete()
            
            # Reorder remaining authors
            remaining_authors = submission.authors.all().order_by('order')
            for order, auth in enumerate(remaining_authors, start=1):
                auth.order = order
                auth.save(update_fields=['order'])
            
            return Response(status=status.HTTP_204_NO_CONTENT)

    # =============================================
    # CORRESPONDENCE
    # =============================================

    @action(detail=True, methods=['get', 'post'], url_path='correspondence')
    def correspondence(self, request, pk=None):
        """
        GET:  List all correspondence for this submission.
        POST: Author sends a message to the editor.
        """
        submission = self.get_object()

        if request.method == 'GET':
            messages = submission.correspondence.all()
            # Mark editor/system messages as read when author fetches
            unread = messages.filter(
                is_read=False,
                message_type__in=[
                    Correspondence.MessageType.EDITOR_TO_AUTHOR,
                    Correspondence.MessageType.DECISION_LETTER,
                    Correspondence.MessageType.SYSTEM,
                ],
            )
            from django.utils import timezone as tz
            unread.update(is_read=True, read_at=tz.now())

            serializer = CorrespondenceSerializer(messages, many=True)
            return success_response(
                data=serializer.data,
                message=_('Correspondence retrieved successfully'),
            )

        # POST – author sends message
        if submission.status == Submission.Status.DRAFT:
            return validation_error_response(
                _('Cannot send messages for draft submissions.')
            )

        ser = CorrespondenceCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        msg = Correspondence.objects.create(
            submission=submission,
            sender=request.user,
            message_type=Correspondence.MessageType.AUTHOR_TO_EDITOR,
            subject=ser.validated_data.get('subject', ''),
            body=ser.validated_data['body'],
        )

        try:
            from apps.notifications.email_service import _send
            from apps.notifications.models import EmailLog
            editor = submission.assigned_editor
            if editor and editor.email:
                _send(
                    email_type=EmailLog.EmailType.OTHER,
                    recipient_email=editor.email,
                    subject=f'New message from author — {submission.manuscript_id}',
                    template_name='status_change',
                    context={
                        'user_name': editor.full_name or editor.email,
                        'manuscript_id': submission.manuscript_id,
                        'title': submission.title,
                        'old_status': 'Message',
                        'new_status': 'New author correspondence',
                        'notes': msg.body[:200],
                    },
                    recipient_user=editor,
                    submission=submission,
                )
        except Exception as e:
            logger.warning(f"Correspondence email failed: {e}")

        return created_response(
            data=CorrespondenceSerializer(msg).data,
            message=_('Message sent successfully'),
        )
