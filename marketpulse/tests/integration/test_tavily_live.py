"""
Live integration test for Tavily Search API.
Executes a real query against Tavily Search API when TAVILY_API_KEY is configured.
"""

import os
import pytest
from app.config import settings
from app.services.web_search.client import TavilySearchClient
from app.services.web_search.search import search_web

# Only run if real key is configured and RUN_LIVE_TAVILY_TEST=1 or key starts with tvly-
HAS_TAVILY_KEY = bool(
    settings.TAVILY_API_KEY
    and settings.TAVILY_API_KEY.startswith("tvly-")
    and "your" not in settings.TAVILY_API_KEY.lower()
)


@pytest.mark.skipif(
    not (HAS_TAVILY_KEY and os.getenv("RUN_LIVE_TAVILY_TEST") == "1"),
    reason="Live Tavily Search API test. Set RUN_LIVE_TAVILY_TEST=1 with valid TAVILY_API_KEY in .env to run.",
)
def test_tavily_live_search():
    """Verify actual live connection to Tavily Search API."""
    query = "Bangladesh digital payments bKash market share"
    results = search_web(query, max_results=3, search_depth="basic")

    assert len(results) > 0
    first = results[0]
    assert first["evidence_id"]
    assert first["title"]
    assert first["url"].startswith(("http://", "https://"))
    assert first["search_provider"] == "tavily"
    assert first["source_type"] == "tavily_search"
    assert first["publisher"]
    print(f"\n[LIVE TAVILY SUCCESS] Found {len(results)} sources for '{query}'")
    for r in results:
        print(f"  - {r['title']} ({r['publisher']}) -> {r['url']}")
