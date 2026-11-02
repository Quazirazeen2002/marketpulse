"""
Typed exceptions for MARKETPULSE web search service.
Ensures explicit, granular error handling instead of generic or silent failures.
"""


class WebSearchError(Exception):
    """Base exception for all web search operations."""
    def __init__(self, message: str, provider: str = "tavily", query: str = ""):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.query = query


class SearchAuthError(WebSearchError):
    """Raised when Tavily API key is missing, unauthorized, or invalid."""
    pass


class SearchRateLimitError(WebSearchError):
    """Raised when Tavily rate limits or usage quota are exceeded."""
    pass


class SearchTimeoutError(WebSearchError):
    """Raised when Tavily search times out."""
    pass


class SearchBudgetExceededError(WebSearchError):
    """Raised when a research run exceeds its allocated search budget."""
    def __init__(self, message: str, research_id: str = "", current_count: int = 0, max_budget: int = 15):
        super().__init__(message, provider="tavily")
        self.research_id = research_id
        self.current_count = current_count
        self.max_budget = max_budget


class InvalidQueryError(WebSearchError):
    """Raised when the search query is empty, malformed, or invalid."""
    pass


class EmptySearchResultsError(WebSearchError):
    """Raised when a search executes successfully but yields zero results."""
    pass
