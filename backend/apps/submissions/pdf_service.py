"""
TruEditor - PDF Generation Service
====================================
Generates submission PDF using WeasyPrint.
Stores the generated PDF in the configured storage backend (S3/R2/local).

Developer: Abdullah Dogan
"""

import logging
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.files.base import ContentFile

from .models import Submission
from apps.files.models import ManuscriptFile

logger = logging.getLogger(__name__)

LANGUAGE_DISPLAY = {'en': 'English', 'tr': 'Turkish'}


def generate_submission_pdf(submission: Submission, user=None) -> ManuscriptFile:
    """
    Generate a PDF for the given submission and store it as a ManuscriptFile.

    Tries WeasyPrint first; falls back to a lightweight HTML-only approach
    if WeasyPrint system dependencies are unavailable.

    Returns the created ManuscriptFile instance.
    """
    html = _render_html(submission)
    pdf_bytes = _html_to_pdf(html)

    # Remove any previously generated system PDF for this submission
    ManuscriptFile.objects.filter(
        submission=submission,
        file_type='system_pdf',
        is_active=True,
    ).update(is_active=False)

    filename = f"{submission.manuscript_id or 'DRAFT'}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_obj = ContentFile(pdf_bytes, name=filename)

    manuscript_file = ManuscriptFile.objects.create(
        submission=submission,
        uploaded_by=user,
        file=file_obj,
        file_type='system_pdf',
        original_filename=filename,
        file_size=len(pdf_bytes),
        mime_type='application/pdf',
        description='Auto-generated submission PDF',
        is_primary=False,
        order=9999,
    )

    logger.info(
        "PDF generated for submission %s (%s bytes)",
        submission.manuscript_id or submission.id,
        len(pdf_bytes),
    )
    return manuscript_file


def _render_html(submission: Submission) -> str:
    authors = submission.authors.all().order_by('order')
    files = submission.files.filter(is_active=True).order_by('order')
    corresponding = submission.get_corresponding_author()

    context = {
        'title': submission.title,
        'title_en': submission.title_en,
        'abstract': submission.abstract,
        'abstract_en': submission.abstract_en,
        'keywords': submission.keywords or [],
        'keywords_en': submission.keywords_en or [],
        'language': submission.language,
        'language_display': LANGUAGE_DISPLAY.get(submission.language, submission.language),
        'article_type_display': submission.get_article_type_display(),
        'manuscript_id': submission.manuscript_id or 'DRAFT',
        'submitted_at': (
            submission.submitted_at.strftime('%B %d, %Y')
            if submission.submitted_at else None
        ),
        'generated_at': timezone.now().strftime('%B %d, %Y at %H:%M'),
        'authors': authors,
        'corresponding_author': corresponding,
        'files': files,
        'cover_letter': submission.cover_letter,
        'ethics_statement': submission.ethics_statement,
        'ethics_approval_number': submission.ethics_approval_number,
        'conflict_of_interest': submission.conflict_of_interest,
        'funding_statement': submission.funding_statement,
    }

    return render_to_string('pdf/submission.html', context)


def _html_to_pdf(html: str) -> bytes:
    """Convert HTML to PDF bytes using WeasyPrint."""
    from weasyprint import HTML
    pdf = HTML(string=html).write_pdf()
    logger.debug("PDF generated with WeasyPrint")
    return pdf
