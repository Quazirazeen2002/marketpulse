"""
Web Search Service for MARKETPULSE.
Integrates Tavily Search API with cost-optimized caching, deduplication,
run-level budget limits, and evidence normalization.
"""

from app.services.web_search.exceptions import (
    WebSearchError,
    SearchAuthError,
    SearchRateLimitError,
    SearchTimeoutError,
    SearchBudgetExceededError,
    InvalidQueryError,
    EmptySearchResultsError,
)
from app.services.web_search.normalizer import (
    normalize_tavily_result,
    normalize_tavily_response,
    generate_evidence_id,
    extract_publisher_from_url,
)
from app.services.web_search.client import (
    TavilySearchClient,
    tavily_search_client,
)
from app.services.web_search.cache import (
    SearchCache,
    search_cache,
    generate_cache_key,
)
from app.services.web_search.search import (
    search_web,
    budget_manager,
    ResearchSearchBudget,
)

__all__ = [
    "search_web",
    "tavily_search_client",
    "TavilySearchClient",
    "search_cache",
    "SearchCache",
    "budget_manager",
    "ResearchSearchBudget",
    "generate_cache_key",
    "normalize_tavily_result",
    "normalize_tavily_response",
    "generate_evidence_id",
    "extract_publisher_from_url",
    "WebSearchError",
    "SearchAuthError",
    "SearchRateLimitError",
    "SearchTimeoutError",
    "SearchBudgetExceededError",
    "InvalidQueryError",
    "EmptySearchResultsError",
]
