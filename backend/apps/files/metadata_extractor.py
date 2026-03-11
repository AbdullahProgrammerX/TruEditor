"""
TruEditor - Metadata Extractor
================================
Extracts title, abstract, and keywords from uploaded DOCX and PDF files.
Supports both English and Turkish academic document conventions.
"""

import io
import re
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional

logger = logging.getLogger(__name__)

ABSTRACT_HEADINGS = re.compile(
    r'^(?:abstract|özet|öz)\s*[:\-]?\s*$',
    re.IGNORECASE,
)

ABSTRACT_INLINE = re.compile(
    r'^(?:abstract|özet|öz)\s*[:\-]\s*(.+)',
    re.IGNORECASE | re.DOTALL,
)

KEYWORDS_PATTERN = re.compile(
    r'^(?:keywords?|anahtar\s*kelimeler?|anahtar\s*sözcükler?)\s*[:\-]\s*(.+)',
    re.IGNORECASE,
)

SECTION_HEADINGS = re.compile(
    r'^(?:\d+[\.\)]\s*)?(?:introduction|giriş|background|arka\s*plan|methods?|yöntem|materyal|results?|bulgular|discussion|tartışma|conclusion|sonuç|references|kaynakça)',
    re.IGNORECASE,
)


@dataclass
class ExtractedMetadata:
    title: Optional[str] = None
    abstract: Optional[str] = None
    keywords: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def has_data(self) -> bool:
        return bool(self.title or self.abstract or self.keywords)


def extract_from_docx(file_obj) -> ExtractedMetadata:
    """Extract metadata from a DOCX file."""
    try:
        import docx
    except ImportError:
        logger.warning("python-docx not installed")
        return ExtractedMetadata()

    meta = ExtractedMetadata()

    try:
        file_obj.seek(0)
        doc = docx.Document(io.BytesIO(file_obj.read()))
    except Exception as exc:
        logger.warning("Failed to open DOCX: %s", exc)
        return meta

    props = doc.core_properties
    if props.title and len(props.title.strip()) > 3:
        meta.title = props.title.strip()

    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        return meta

    if not meta.title:
        meta.title = _guess_title_from_paragraphs(paragraphs)

    meta.abstract = _find_abstract(paragraphs)
    meta.keywords = _find_keywords(paragraphs)

    return meta


def extract_from_pdf(file_obj) -> ExtractedMetadata:
    """Extract metadata from a PDF file (basic)."""
    try:
        import pdfplumber
    except ImportError:
        logger.warning("pdfplumber not installed")
        return ExtractedMetadata()

    meta = ExtractedMetadata()

    try:
        file_obj.seek(0)
        pdf = pdfplumber.open(io.BytesIO(file_obj.read()))
    except Exception as exc:
        logger.warning("Failed to open PDF: %s", exc)
        return meta

    pdf_meta = pdf.metadata or {}
    title = pdf_meta.get('Title', '') or pdf_meta.get('title', '')
    if title and len(title.strip()) > 3:
        meta.title = title.strip()

    text_lines: list[str] = []
    for page in pdf.pages[:3]:
        page_text = page.extract_text()
        if page_text:
            text_lines.extend(
                line.strip() for line in page_text.split('\n') if line.strip()
            )

    pdf.close()

    if not text_lines:
        return meta

    if not meta.title:
        meta.title = _guess_title_from_paragraphs(text_lines)

    meta.abstract = _find_abstract(text_lines)
    meta.keywords = _find_keywords(text_lines)

    return meta


def extract_metadata(file_obj, filename: str) -> ExtractedMetadata:
    """
    Main entry point. Dispatches based on file extension.
    Returns ExtractedMetadata (always safe, never raises).
    """
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    try:
        if ext in ('docx', 'doc'):
            return extract_from_docx(file_obj)
        elif ext == 'pdf':
            return extract_from_pdf(file_obj)
    except Exception as exc:
        logger.error("Metadata extraction failed for %s: %s", filename, exc)

    return ExtractedMetadata()


# ── Helper functions ──────────────────────────────────────


def _guess_title_from_paragraphs(paragraphs: list[str]) -> Optional[str]:
    """
    Heuristic: the title is usually one of the first non-trivial lines
    that isn't a section heading and is reasonably short.
    """
    for line in paragraphs[:8]:
        if len(line) < 5:
            continue
        if ABSTRACT_HEADINGS.match(line):
            break
        if KEYWORDS_PATTERN.match(line):
            continue
        if SECTION_HEADINGS.match(line):
            break
        if _looks_like_author_line(line):
            continue
        if 10 < len(line) < 300:
            return line

    return None


def _find_abstract(paragraphs: list[str]) -> Optional[str]:
    """Find the abstract section by heading or inline pattern."""
    collecting = False
    parts: list[str] = []

    for line in paragraphs:
        if ABSTRACT_HEADINGS.match(line):
            collecting = True
            continue

        m = ABSTRACT_INLINE.match(line)
        if m:
            parts.append(m.group(1).strip())
            collecting = True
            continue

        if collecting:
            if KEYWORDS_PATTERN.match(line):
                break
            if SECTION_HEADINGS.match(line):
                break
            if ABSTRACT_HEADINGS.match(line):
                break
            parts.append(line)

            if len(' '.join(parts)) > 3000:
                break

    abstract = ' '.join(parts).strip()
    return abstract if len(abstract) > 20 else None


def _find_keywords(paragraphs: list[str]) -> list[str]:
    """Find keywords line and split into list."""
    for line in paragraphs:
        m = KEYWORDS_PATTERN.match(line)
        if m:
            raw = m.group(1)
            raw = raw.rstrip('.')
            separators = [';', ',', '·', '•', '|']
            for sep in separators:
                if sep in raw:
                    return [kw.strip() for kw in raw.split(sep) if kw.strip()]
            words = [kw.strip() for kw in raw.split(',') if kw.strip()]
            return words if words else [raw.strip()]

    return []


def _looks_like_author_line(line: str) -> bool:
    """Simple heuristic: lines with multiple commas and short segments."""
    if '@' in line or 'orcid' in line.lower():
        return True
    if line.count(',') >= 2 and all(len(s.strip()) < 40 for s in line.split(',')):
        return True
    if re.match(r'^[\w\s\.,]+\d{1,2}\s*$', line):
        return True
    return False
