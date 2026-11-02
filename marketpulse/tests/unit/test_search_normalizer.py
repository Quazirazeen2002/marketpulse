"""
Unit tests for Tavily search result normalizer.
Verifies schema compliance, deterministic ID hashing, metadata preservation,
URL deduplication, and publisher attribution.
"""

import pytest
from app.services.web_search.normalizer import (
    normalize_tavily_result,
    normalize_tavily_response,
    generate_evidence_id,
    extract_publisher_from_url,
)


def test_generate_evidence_id_deterministic():
    url1 = "https://example.com/reports/market-2026"
    url2 = "https://example.com/reports/market-2026/"
    # Trailing slash stripped
    assert generate_evidence_id(url1) == generate_evidence_id(url2)
    assert len(generate_evidence_id(url1)) == 16


def test_extract_publisher_from_url():
    assert extract_publisher_from_url("https://www.reuters.com/business/tech") == "reuters.com"
    assert extract_publisher_from_url("http://bloomberg.com/news") == "bloomberg.com"
    assert extract_publisher_from_url("invalid-url") == "Unknown Publisher"



def test_normalize_tavily_result_valid():
    raw_item = {
        "title": "E-Commerce Market Growth in South Asia",
        "url": "https://www.statista.com/outlook/dmo/ecommerce/bangladesh",
        "content": "The e-commerce market in Bangladesh is projected to grow by 18.2% annually.",
        "score": 0.892,
        "published_date": "2026-01-10",
        "raw_content": "Full raw text content here...",
    }

    norm = normalize_tavily_result(raw_item, query="Bangladesh ecommerce growth")
    assert norm is not None
    assert norm["title"] == "E-Commerce Market Growth in South Asia"
    assert norm["url"] == "https://www.statista.com/outlook/dmo/ecommerce/bangladesh"
    assert norm["publisher"] == "statista.com"
    assert norm["score"] == 0.892
    assert norm["query"] == "Bangladesh ecommerce growth"
    assert norm["search_provider"] == "tavily"
    assert norm["source_type"] == "tavily_search"
    assert norm["published_date"] == "2026-01-10"
    assert len(norm["evidence_id"]) == 16
    assert norm["raw_content"] == "Full raw text content here..."


def test_normalize_tavily_result_invalid():
    # Missing URL
    assert normalize_tavily_result({"title": "No URL"}) is None
    # Invalid protocol
    assert normalize_tavily_result({"url": "ftp://files.org/doc"}) is None
    # Non-dict
    assert normalize_tavily_result("not a dict") is None  # type: ignore


def test_normalize_tavily_response_deduplication_and_limit():
    raw_response = {
        "query": "market competitors",
        "results": [
            {"title": "Comp A", "url": "https://company.com/a", "content": "Text A"},
            {"title": "Comp A Dupe", "url": "https://company.com/a", "content": "Text A duplicate"},
            {"title": "Comp B", "url": "https://company.com/b", "content": "Text B"},
            {"title": "Comp C", "url": "https://company.com/c", "content": "Text C"},
            {"title": "Comp D", "url": "https://company.com/d", "content": "Text D"},
        ]
    }

    normalized = normalize_tavily_response(raw_response, query="market competitors", max_results=2)
    # Deduplication eliminated the duplicate URL
    # max_results truncated to 2
    assert len(normalized) == 2
    assert normalized[0]["url"] == "https://company.com/a"
    assert normalized[1]["url"] == "https://company.com/b"
