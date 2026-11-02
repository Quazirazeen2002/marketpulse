"""
Core Web Search Service for MARKETPULSE.
Orchestrates Tavily API queries with research-level budgets, query deduplication,
dual-tier caching, and comprehensive error handling.
"""

import logging
import threading
from typing import List, Dict, Any, Optional

from app.config import settings
from app.services.web_search.client import tavily_search_client
from app.services.web_search.cache import (
    search_cache,
    generate_cache_key,
    normalize_query_string,
)
from app.services.web_search.exceptions import (
    WebSearchError,
    SearchAuthError,
    SearchRateLimitError,
    SearchTimeoutError,
    SearchBudgetExceededError,
    InvalidQueryError,
    EmptySearchResultsError,
)

logger = logging.getLogger(__name__)


class ResearchSearchBudget:
    """
    Thread-safe run-level search budget manager.
    Enforces shared budget ceilings across parallel specialist agents.
    """

    def __init__(self, max_searches_per_run: int = 15):
        self.default_max = max_searches_per_run
        self._lock = threading.Lock()
        # research_id -> count of executed API searches
        self._counts: Dict[str, int] = {}
        # research_id -> list of executed queries
        self._history: Dict[str, List[str]] = {}

    def get_count(self, research_id: str) -> int:
        with self._lock:
            return self._counts.get(research_id, 0)

    def can_search(self, research_id: str, max_searches: Optional[int] = None) -> bool:
        limit = max_searches if max_searches is not None else self.default_max
        with self._lock:
            return self._counts.get(research_id, 0) < limit

    def record_search(self, research_id: str, query: str, max_searches: Optional[int] = None):
        """Record an API search; raises SearchBudgetExceededError if over ceiling."""
        limit = max_searches if max_searches is not None else self.default_max
        with self._lock:
            current = self._counts.get(research_id, 0)
            if current >= limit:
                raise SearchBudgetExceededError(
                    f"Research run '{research_id}' exceeded search budget of {limit} queries.",
                    research_id=research_id,
                    current_count=current,
                    max_budget=limit,
                )
            self._counts[research_id] = current + 1
            if research_id not in self._history:
                self._history[research_id] = []
            self._history[research_id].append(query)

    def get_run_stats(self, research_id: str) -> Dict[str, Any]:
        with self._lock:
            count = self._counts.get(research_id, 0)
            history = list(self._history.get(research_id, []))
            return {
                "research_id": research_id,
                "searches_executed": count,
                "budget_limit": self.default_max,
                "remaining_budget": max(0, self.default_max - count),
                "query_history": history,
            }

    def reset_run(self, research_id: str):
        with self._lock:
            self._counts.pop(research_id, None)
            self._history.pop(research_id, None)


# Global research budget tracker
budget_manager = ResearchSearchBudget(
    max_searches_per_run=settings.MAX_SEARCHES_PER_RESEARCH
)


def _generate_mock_search_results(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """Return deterministic mock results when ENABLE_MOCK_MODE is active."""
    import hashlib
    clean_query = query.strip()
    results = []
    for i in range(1, min(max_results + 1, 5)):
        url = f"https://example-market-intel.org/{clean_query.replace(' ', '-').lower()}-analysis-{i}"
        ev_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        results.append({
            "evidence_id": ev_id,
            "title": f"Verified Industry Report on {clean_query.title()} (Part {i})",
            "url": url,
            "content": f"Comprehensive empirical market finding {i}: detailed assessment regarding {clean_query}.",
            "publisher": "example-market-intel.org",
            "score": round(0.95 - (i * 0.05), 4),
            "query": clean_query,
            "search_provider": "tavily",
            "source_type": "tavily_search",
            "published_date": "2026-01-15",
        })
    return results


def search_web(
    query: str,
    max_results: int = 8,
    search_depth: Optional[str] = None,
    topic: str = "general",
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    research_id: Optional[str] = None,
    **kwargs: Any,
) -> List[Dict[str, Any]]:
    """
    Search the web using Tavily Search API with cost optimization and caching.

    Parameters:
        query: The search term.
        max_results: Number of results to retrieve (defaults to 8).
        search_depth: 'basic' or 'advanced' (defaults to settings.TAVILY_SEARCH_DEPTH).
        topic: 'general', 'news', or 'finance' (defaults to settings.TAVILY_TOPIC).
        include_domains: Optional list of domains to filter by.
        exclude_domains: Optional list of domains to exclude.
        research_id: Optional research run ID for budget enforcement & run deduplication.
        **kwargs: Backwards compatibility (e.g. limit=N).

    Returns:
        List of normalized search result dictionaries.

    Raises:
        SearchBudgetExceededError: When research run has exhausted budget.
        SearchAuthError: On invalid or missing API key.
        SearchRateLimitError: When Tavily quota/rate limits are hit.
        SearchTimeoutError: When request times out.
        InvalidQueryError: For empty or invalid query.
        EmptySearchResultsError: When no results are found.
        WebSearchError: On unexpected provider errors.
    """
    # Support 'limit' keyword argument for backwards compatibility
    if "limit" in kwargs and max_results == 8:
        max_results = kwargs["limit"]

    if not query or not query.strip():
        raise InvalidQueryError("Search query cannot be empty.", provider="tavily")

    clean_query = query.strip()
    depth = search_depth or settings.TAVILY_SEARCH_DEPTH or "basic"
    search_topic = topic or settings.TAVILY_TOPIC or "general"
    limit = min(max_results, settings.MAX_RESULTS_PER_SEARCH or 10)

    # 1. Mock mode check
    if settings.ENABLE_MOCK_MODE:
        logger.info("[Mock Search] Returning simulated results for '%s'", clean_query)
        return _generate_mock_search_results(clean_query, max_results=limit)

    # 2. Compute Cache Key
    cache_key = generate_cache_key(
        query=clean_query,
        search_depth=depth,
        topic=search_topic,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        max_results=limit,
    )

    # 3. Check within-run duplicate or general cache
    cached_results = search_cache.get(cache_key)
    if cached_results:
        logger.info(
            "Search Cache HIT | query='%s' | count=%s | research_id=%s",
            clean_query,
            len(cached_results),
            research_id or "global",
        )
        if research_id:
            search_cache.record_run_query(research_id, clean_query)
        return cached_results[:limit]

    # 4. Enforce Research-Level Search Budget
    if research_id:
        # Check budget ceiling before making network request
        budget_manager.record_search(
            research_id=research_id,
            query=clean_query,
            max_searches=settings.MAX_SEARCHES_PER_RESEARCH,
        )

    # 5. Execute Tavily Search via Client
    try:
        results = tavily_search_client.search(
            query=clean_query,
            max_results=limit,
            search_depth=depth,
            topic=search_topic,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            include_raw_content=settings.TAVILY_INCLUDE_RAW_CONTENT,
        )

        # Store in cache
        search_cache.set(
            cache_key=cache_key,
            query=clean_query,
            results=results,
            search_depth=depth,
            topic=search_topic,
        )

        if research_id:
            search_cache.record_run_query(research_id, clean_query)

        return results

    except Exception:
        # Re-raise typed exceptions directly
        raise
