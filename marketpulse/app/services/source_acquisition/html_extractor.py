import logging
from typing import Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup
import trafilatura
from .content_normalizer import normalize_content_text

logger = logging.getLogger(__name__)


def extract_html_content(
    html: str,
    base_url: str = "",
) -> Tuple[str, Dict[str, Any], str]:
    """
    Extract readable text content and metadata from HTML.
    Uses Trafilatura as primary extractor with BeautifulSoup fallback.
    Returns: (extracted_text, metadata_dict, status_str)
    """
    if not html or not html.strip():
        return "", {}, "extraction_failed"

    metadata: Dict[str, Any] = {
        "title": None,
        "author": None,
        "date": None,
        "sitename": None,
        "canonical_url": None,
    }

    # 1. Try Trafilatura extraction
    extracted_text = ""
    try:
        trafilatura_result = trafilatura.extract(
            html,
            url=base_url,
            include_comments=False,
            include_tables=True,
            include_links=False,
            output_format="txt",
        )
        if trafilatura_result and len(trafilatura_result.strip()) > 80:
            extracted_text = normalize_content_text(trafilatura_result)

        # Extract metadata via Trafilatura
        trafilatura_meta = trafilatura.extract_metadata(html, default_url=base_url)
        if trafilatura_meta:
            metadata["title"] = trafilatura_meta.title
            metadata["author"] = trafilatura_meta.author
            metadata["date"] = trafilatura_meta.date
            metadata["sitename"] = trafilatura_meta.sitename
            metadata["canonical_url"] = trafilatura_meta.url
    except Exception as exc:
        logger.debug("Trafilatura extraction exception: %s", exc)

    # 2. BeautifulSoup Fallback or metadata enrichment
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Fill missing title
        if not metadata["title"]:
            title_tag = soup.find("title") or soup.find("h1")
            if title_tag:
                metadata["title"] = title_tag.get_text(strip=True)

        # Fill canonical URL
        if not metadata["canonical_url"]:
            canonical_tag = soup.find("link", rel=lambda x: x and "canonical" in x.lower())
            if canonical_tag and canonical_tag.get("href"):
                metadata["canonical_url"] = canonical_tag.get("href").strip()

        # If Trafilatura produced too little text, use BeautifulSoup article/p extraction
        if not extracted_text or len(extracted_text) < 100:
            # Strip non-content tags
            for tag in soup(["script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form"]):
                tag.decompose()

            # Find main article container if available
            article = soup.find("article") or soup.find("main") or soup.find(id=lambda x: x and "content" in x.lower())
            target = article if article else soup.body or soup

            paragraphs = [p.get_text(strip=True) for p in target.find_all(["p", "h2", "h3", "li"])]
            bs_text = "\n\n".join(p for p in paragraphs if len(p) > 25)

            if len(bs_text.strip()) > len(extracted_text):
                extracted_text = normalize_content_text(bs_text)
    except Exception as exc:
        logger.debug("BeautifulSoup fallback exception: %s", exc)

    if not extracted_text:
        return "", metadata, "extraction_failed"

    status = "retrieved_full_text" if len(extracted_text) > 300 else "retrieved_partial"
    return extracted_text, metadata, status
