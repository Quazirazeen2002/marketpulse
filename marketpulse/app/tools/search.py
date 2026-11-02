"""
Web Search tool interface for MARKETPULSE.
Replaced Meta Web Search with Tavily Search API.
Provides backwards-compatible interface delegating to app.services.web_search.
"""

from app.services.web_search import (
    search_web,
    tavily_search_client,
    budget_manager,
    search_cache,
    WebSearchError,
    SearchAuthError,
    SearchRateLimitError,
    SearchTimeoutError,
    SearchBudgetExceededError,
    InvalidQueryError,
    EmptySearchResultsError,
)

__all__ = [
    "search_web",
    "tavily_search_client",
    "budget_manager",
    "search_cache",
    "WebSearchError",
    "SearchAuthError",
    "SearchRateLimitError",
    "SearchTimeoutError",
    "SearchBudgetExceededError",
    "InvalidQueryError",
    "EmptySearchResultsError",
]
