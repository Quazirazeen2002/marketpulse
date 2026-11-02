import io
import logging
from typing import Dict, Any, Tuple
import fitz  # PyMuPDF
from .content_normalizer import normalize_content_text

logger = logging.getLogger(__name__)


def extract_pdf_content(
    pdf_bytes: bytes,
    max_pages: int = 30,
) -> Tuple[str, Dict[int, str], Dict[str, Any], str]:
    """
    Extract text and page-by-page mapping from PDF bytes.
    Returns: (full_text, pages_dict, metadata, status)
    """
    if not pdf_bytes:
        return "", {}, {}, "extraction_failed"

    pages_dict: Dict[int, str] = {}
    metadata: Dict[str, Any] = {
        "title": None,
        "author": None,
        "page_count": 0,
    }

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        metadata["page_count"] = len(doc)
        doc_meta = doc.metadata or {}
        metadata["title"] = doc_meta.get("title") or None
        metadata["author"] = doc_meta.get("author") or None

        total_pages = min(len(doc), max_pages)
        for page_num in range(total_pages):
            page = doc[page_num]
            page_text = normalize_content_text(page.get_text("text"))
            if page_text:
                pages_dict[page_num + 1] = page_text

        doc.close()

        full_text = "\n\n".join(
            f"--- [Page {p}] ---\n{text}" for p, text in sorted(pages_dict.items())
        )

        if not full_text.strip():
            return "", {}, metadata, "extraction_failed"

        status = "retrieved_full_text" if len(pages_dict) == metadata["page_count"] else "retrieved_partial"
        return full_text, pages_dict, metadata, status

    except Exception as exc:
        logger.warning("PDF extraction failed: %s", exc)
        return "", {}, metadata, "extraction_failed"
