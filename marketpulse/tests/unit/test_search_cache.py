"""
Unit tests for SearchCache and query deduplication.
Tests cache key determinism, hit/miss tracking, TTL expiration, and run-level deduplication.
"""

import time
import pytest
from app.services.web_search.cache import (
    SearchCache,
    generate_cache_key,
    normalize_query_string,
)


def test_normalize_query_string():
    assert normalize_query_string("  Bangladesh   E-Commerce Trends  ") == "bangladesh e-commerce trends"


def test_generate_cache_key_determinism():
    k1 = generate_cache_key("Fintech in UK", search_depth="basic", topic="finance", include_domains=["bloomberg.com", "reuters.com"])
    k2 = generate_cache_key("  fintech  in  uk ", search_depth="basic", topic="finance", include_domains=["reuters.com", "bloomberg.com"])
    # Same normalized parameters produce identical hash key
    assert k1 == k2


def test_search_cache_hit_and_miss():
    cache = SearchCache(ttl_hours=1, enabled=True)
    cache.clear()

    key = f"test_key_{time.time_ns()}"
    assert cache.get(key) is None
    assert cache.misses == 1
    assert cache.hits == 0

    mock_results = [{"title": "Cached Title", "url": "https://example.com/item"}]
    cache.set(key, query="test query", results=mock_results)

    cached = cache.get(key)
    assert cached is not None
    assert len(cached) == 1
    assert cached[0]["title"] == "Cached Title"
    assert cache.hits == 1

    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["hit_rate_pct"] == 50.0


def test_search_cache_ttl_expiration():
    # Cache with 0 hours TTL (immediate expiration)
    cache = SearchCache(ttl_hours=0, enabled=True)
    cache.clear()

    key = f"expire_key_{time.time_ns()}"
    cache.set(key, query="expired", results=[{"url": "https://exp.com"}])

    # Manually backdate expiration in memory
    cache._memory_cache[key]["expires_at"] = time.time() - 10

    # Should detect expiration and return None
    assert cache.get(key) is None


def test_run_level_query_deduplication():
    cache = SearchCache(ttl_hours=24, enabled=True)
    cache.clear()

    run_id = "run-session-abc"
    query = "Daraz Bangladesh market share"

    assert not cache.is_query_executed_in_run(run_id, query)
    cache.record_run_query(run_id, query)
    assert cache.is_query_executed_in_run(run_id, query)
    # Different run ID is isolated
    assert not cache.is_query_executed_in_run("other-run", query)
