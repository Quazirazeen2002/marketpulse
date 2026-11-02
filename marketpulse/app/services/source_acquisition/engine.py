import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Dict, Any

from app.schemas import SourceDocument, SourceAcquisitionStatus
from .url_validator import normalize_url, get_domain, is_valid_http_url
from .fetcher import fetch_url
from .html_extractor import extract_html_content
from .pdf_extractor import extract_pdf_content
from .content_normalizer import compute_content_hash, truncate_text, normalize_content_text

logger = logging.getLogger(__name__)


def acquire_source(
    url: str,
    fallback_title: str = "Untitled Source",
    fallback_snippet: str = "",
    source_id: Optional[str] = None,
    fetch_content: bool = True,
    search_provider: str = "tavily",
) -> SourceDocument:
    """
    Acquire and extract full text for a given source URL.
    Gracefully falls back to snippet_only or inaccessible without fabricating text.
    """
    clean_url = normalize_url(url)
    domain = get_domain(clean_url)
    sid = source_id or hashlib.sha256(clean_url.encode("utf-8")).hexdigest()[:16]

    if not is_valid_http_url(clean_url):
        return SourceDocument(
            source_id=sid,
            url=url,
            title=fallback_title,
            publisher=domain,
            extraction_status=SourceAcquisitionStatus.INACCESSIBLE,
            extracted_text=fallback_snippet or fallback_title,
            content_hash=compute_content_hash(fallback_snippet or fallback_title),
            error_message="Invalid HTTP/HTTPS URL format",
            search_provider=search_provider,
        )

    if not fetch_content:
        return SourceDocument(
            source_id=sid,
            url=clean_url,
            canonical_url=clean_url,
            title=fallback_title,
            publisher=domain,
            extraction_status=SourceAcquisitionStatus.SNIPPET_ONLY,
            extracted_text=normalize_content_text(fallback_snippet or fallback_title),
            content_hash=compute_content_hash(fallback_snippet or fallback_title),
            content_type="text/html",
            search_provider=search_provider,
        )

    # Attempt fetch
    content_bytes, content_type, http_status, error_msg = fetch_url(clean_url)

    # Handle fetch failure
    if not content_bytes or error_msg:
        status = (
            SourceAcquisitionStatus.SNIPPET_ONLY
            if fallback_snippet
            else SourceAcquisitionStatus.INACCESSIBLE
        )
        return SourceDocument(
            source_id=sid,
            url=clean_url,
            canonical_url=clean_url,
            title=fallback_title,
            publisher=domain,
            extraction_status=status,
            extracted_text=normalize_content_text(fallback_snippet or fallback_title),
            content_hash=compute_content_hash(fallback_snippet or fallback_title),
            http_status=http_status,
            error_message=error_msg,
            search_provider=search_provider,
        )

    # 1. PDF Resource
    is_pdf = clean_url.lower().endswith(".pdf") or "application/pdf" in content_type
    if is_pdf:
        full_text, pages_dict, meta, status_str = extract_pdf_content(content_bytes)
        status_enum = (
            SourceAcquisitionStatus.RETRIEVED_FULL_TEXT
            if status_str == "retrieved_full_text"
            else SourceAcquisitionStatus.RETRIEVED_PARTIAL
            if status_str == "retrieved_partial"
            else SourceAcquisitionStatus.EXTRACTION_FAILED
        )

        extracted_text, is_truncated = truncate_text(full_text)
        return SourceDocument(
            source_id=sid,
            url=clean_url,
            canonical_url=clean_url,
            title=meta.get("title") or fallback_title,
            publisher=domain,
            author=meta.get("author"),
            extraction_status=status_enum,
            extracted_text=extracted_text or fallback_snippet,
            content_hash=compute_content_hash(extracted_text or fallback_snippet),
            content_type="application/pdf",
            page_count=meta.get("page_count", len(pages_dict)),
            http_status=http_status,
            search_provider=search_provider,
        )

    # 2. HTML Resource
    try:
        html_str = content_bytes.decode("utf-8", errors="replace")
    except Exception:
        html_str = str(content_bytes)

    extracted_text, meta, status_str = extract_html_content(html_str, base_url=clean_url)

    # If extracted text is too sparse, fall back to snippet
    if not extracted_text or len(extracted_text.strip()) < 80:
        status_enum = (
            SourceAcquisitionStatus.SNIPPET_ONLY
            if fallback_snippet
            else SourceAcquisitionStatus.EXTRACTION_FAILED
        )
        final_text = normalize_content_text(fallback_snippet or fallback_title)
    else:
        status_enum = (
            SourceAcquisitionStatus.RETRIEVED_FULL_TEXT
            if status_str == "retrieved_full_text"
            else SourceAcquisitionStatus.RETRIEVED_PARTIAL
        )
        final_text, _ = truncate_text(extracted_text)

    return SourceDocument(
        source_id=sid,
        url=clean_url,
        canonical_url=meta.get("canonical_url") or clean_url,
        title=meta.get("title") or fallback_title,
        publisher=meta.get("sitename") or domain,
        author=meta.get("author"),
        publication_date=meta.get("date"),
        extraction_status=status_enum,
        extracted_text=final_text,
        content_hash=compute_content_hash(final_text),
        content_type="text/html",
        http_status=http_status,
        search_provider=search_provider,
    )


def acquire_sources_batch(
    results: List[Dict[str, Any]],
    max_workers: int = 5,
    fetch_full_content: bool = True,
) -> List[SourceDocument]:
    """
    Acquire multiple source documents in parallel with worker bounding.
    """
    if not results:
        return []

    acquired_docs: List[SourceDocument] = []

    def _worker(item: Dict[str, Any]) -> SourceDocument:
        return acquire_source(
            url=item.get("url", ""),
            fallback_title=item.get("title", "Untitled Source"),
            fallback_snippet=item.get("content", "") or item.get("snippet", ""),
            source_id=item.get("evidence_id"),
            fetch_content=fetch_full_content,
            search_provider=item.get("search_provider", "tavily"),
        )

    if not fetch_full_content or len(results) <= 1:
        for r in results:
            acquired_docs.append(_worker(r))
        return acquired_docs

    with ThreadPoolExecutor(max_workers=min(max_workers, len(results))) as executor:
        futures = {executor.submit(_worker, r): r for r in results}
        for future in as_completed(futures):
            try:
                doc = future.result()
                acquired_docs.append(doc)
            except Exception as exc:
                orig = futures[future]
                clean_url = orig.get("url", "")
                sid = orig.get("evidence_id") or hashlib.sha256(clean_url.encode()).hexdigest()[:16]
                acquired_docs.append(
                    SourceDocument(
                        source_id=sid,
                        url=clean_url,
                        title=orig.get("title", ""),
                        publisher=get_domain(clean_url),
                        extraction_status=SourceAcquisitionStatus.EXTRACTION_FAILED,
                        extracted_text=orig.get("content", ""),
                        content_hash=compute_content_hash(orig.get("content", "")),
                        error_message=str(exc),
                        search_provider=orig.get("search_provider", "tavily"),
                    )
                )

    return acquired_docs


class SourceAcquisitionEngine:
    """Class interface for source acquisition operations."""

    def __init__(self, fetch_full_content: bool = True, max_workers: int = 5):
        self.fetch_full_content = fetch_full_content
        self.max_workers = max_workers

    def acquire(self, url: str, fallback_title: str = "", fallback_snippet: str = "") -> SourceDocument:
        return acquire_source(
            url=url,
            fallback_title=fallback_title,
            fallback_snippet=fallback_snippet,
            fetch_content=self.fetch_full_content,
        )

    def acquire_batch(self, items: List[Dict[str, Any]]) -> List[SourceDocument]:
        return acquire_sources_batch(
            results=items,
            max_workers=self.max_workers,
            fetch_full_content=self.fetch_full_content,
        )
