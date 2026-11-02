"""
Search result normalizer for MARKETPULSE.
Normalizes raw Tavily API responses into the canonical MARKETPULSE research schema.
Preserves metadata and provenance while guaranteeing consistent formatting.
"""

import hashlib
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def extract_publisher_from_url(url: str) -> str:
    """Extract clean domain name as publisher attribution."""
    try:
        netloc = urlparse(url).netloc
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc or "Unknown Publisher"
    except Exception:
        return "Unknown Publisher"


def generate_evidence_id(url: str) -> str:
    """Generate deterministic 16-character SHA-256 evidence identifier from URL."""
    clean_url = url.strip().rstrip("/")
    return hashlib.sha256(clean_url.encode("utf-8")).hexdigest()[:16]


def normalize_tavily_result(item: Dict[str, Any], query: str = "") -> Optional[Dict[str, Any]]:
    """
    Normalize a single raw Tavily search result into canonical schema:
    {
        "evidence_id": "...",
        "title": "...",
        "url": "...",
        "content": "...",
        "publisher": "...",
        "score": 0.0,
        "query": "...",
        "search_provider": "tavily",
        "source_type": "tavily_search",
        "published_date": null
    }
    """
    if not isinstance(item, dict):
        return None

    url = item.get("url") or item.get("link")
    if not url or not isinstance(url, str):
        return None

    clean_url = url.strip()
    if not (clean_url.startswith("http://") or clean_url.startswith("https://")):
        return None

    title = (item.get("title") or "Untitled").strip()
    content = (item.get("content") or item.get("snippet") or "").strip()

    # Extract publisher from domain or Tavily metadata
    publisher = item.get("publisher") or extract_publisher_from_url(clean_url)

    # Relevance score
    score = 0.0
    try:
        raw_score = item.get("score")
        if raw_score is not None:
            score = round(float(raw_score), 4)
    except (ValueError, TypeError):
        score = 0.0

    # Published date (preserve Tavily metadata if provided, never fabricate)
    published_date = item.get("published_date") or item.get("published_at")
    if published_date is not None:
        published_date = str(published_date).strip() or None

    evidence_id = generate_evidence_id(clean_url)

    normalized = {
        "evidence_id": evidence_id,
        "title": title,
        "url": clean_url,
        "content": content,
        "publisher": publisher,
        "score": score,
        "query": query.strip(),
        "search_provider": "tavily",
        "source_type": "tavily_search",
        "published_date": published_date,
    }

    # Retain raw content if fetched by Tavily
    if item.get("raw_content"):
        normalized["raw_content"] = item["raw_content"]

    return normalized


def normalize_tavily_response(
    raw_response: Dict[str, Any],
    query: str = "",
    max_results: int = 8,
) -> List[Dict[str, Any]]:
    """
    Normalize raw Tavily API response dictionary containing 'results'.
    Deduplicates URLs and limits results.
    """
    if not isinstance(raw_response, dict):
        return []

    raw_items = raw_response.get("results") or []
    if not isinstance(raw_items, list):
        return []

    normalized_results: List[Dict[str, Any]] = []
    seen_urls = set()

    for item in raw_items:
        norm = normalize_tavily_result(item, query=query)
        if not norm:
            continue

        url = norm["url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)
        normalized_results.append(norm)

        if len(normalized_results) >= max_results:
            break

    return normalized_results
