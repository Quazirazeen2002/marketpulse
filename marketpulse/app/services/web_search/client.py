"""
Tavily Search API client wrapper for MARKETPULSE.
Manages connection lifecycle, exception handling, rate limiting, and telemetry.
Guarantees resilient search execution with detailed diagnostics.
"""

import time
import logging
import threading
from typing import List, Dict, Any, Optional

from tavily import TavilyClient
from tavily import errors as tavily_errors

from app.config import settings
from app.services.web_search.exceptions import (
    WebSearchError,
    SearchAuthError,
    SearchRateLimitError,
    SearchTimeoutError,
    InvalidQueryError,
    EmptySearchResultsError,
)
from app.services.web_search.normalizer import normalize_tavily_response

logger = logging.getLogger(__name__)


class TavilySearchClient:
    """
    Singleton-style reusable client wrapper for Tavily Search API.
    Maintains telemetry and translates SDK exceptions into domain exceptions.
    """

    def __init__(self, api_key: Optional[str] = None):
        self._api_key = settings.TAVILY_API_KEY if api_key is None else api_key
        self._client: Optional[TavilyClient] = None
        self._lock = threading.Lock()


        # Telemetry metrics
        self.search_requests: int = 0
        self.failed_requests: int = 0
        self.total_results_returned: int = 0
        self.last_response_time_ms: int = 0
        self.last_search_status: str = "idle"
        self.api_usage_data: Dict[str, Any] = {}

    def _get_client(self) -> TavilyClient:
        """Lazily initialize and return the TavilyClient."""
        if not self._api_key:
            raise SearchAuthError(
                "Tavily API key is missing. Set TAVILY_API_KEY in your .env file or configuration.",
                provider="tavily",
            )
        if self._client is None:
            with self._lock:
                if self._client is None:
                    try:
                        self._client = TavilyClient(api_key=self._api_key)
                    except tavily_errors.MissingAPIKeyError as exc:
                        raise SearchAuthError(str(exc), provider="tavily") from exc
                    except Exception as exc:
                        raise WebSearchError(f"Failed to initialize Tavily client: {exc}", provider="tavily") from exc
        return self._client

    def is_connected(self) -> bool:
        """Check if API key is present and configured."""
        return bool(self._api_key and len(self._api_key.strip()) > 5)

    def search(
        self,
        query: str,
        max_results: int = 8,
        search_depth: str = "basic",
        topic: str = "general",
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        include_raw_content: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Execute web search via Tavily Search API.
        
        Raises:
            SearchAuthError: if API key is missing or invalid.
            SearchRateLimitError: if quota/rate limits are exceeded.
            SearchTimeoutError: if the network request times out.
            InvalidQueryError: if query is empty or rejected by API.
            EmptySearchResultsError: if API succeeds with 0 results.
            WebSearchError: on other unexpected API/network failures.
        """
        if not query or not query.strip():
            raise InvalidQueryError("Search query cannot be empty.", provider="tavily")

        client = self._get_client()
        clean_query = query.strip()
        start_time = time.time()

        with self._lock:
            self.search_requests += 1

        logger.info(
            "Executing Tavily search | query='%s' | depth=%s | max_results=%s",
            clean_query,
            search_depth,
            max_results,
        )

        # Build Tavily search kwargs
        search_kwargs: Dict[str, Any] = {
            "query": clean_query,
            "max_results": max_results,
            "search_depth": search_depth if search_depth in ("basic", "advanced") else "basic",
            "topic": topic if topic in ("general", "news", "finance") else "general",
            "include_raw_content": include_raw_content,
            "include_usage": True,
            "timeout": 45,
        }

        if include_domains:
            search_kwargs["include_domains"] = include_domains
        if exclude_domains:
            search_kwargs["exclude_domains"] = exclude_domains

        try:
            raw_response = client.search(**search_kwargs)
            duration_ms = int((time.time() - start_time) * 1000)

            with self._lock:
                self.last_response_time_ms = duration_ms
                self.last_search_status = "success"
                if isinstance(raw_response, dict) and "usage" in raw_response:
                    self.api_usage_data = raw_response["usage"]

            # Normalize results
            normalized = normalize_tavily_response(
                raw_response=raw_response,
                query=clean_query,
                max_results=max_results,
            )

            with self._lock:
                self.total_results_returned += len(normalized)

            if not normalized:
                logger.warning("Tavily returned 0 results for query: '%s'", clean_query)
                raise EmptySearchResultsError(
                    f"Tavily returned zero results for query: '{clean_query}'",
                    provider="tavily",
                    query=clean_query,
                )

            logger.info(
                "Tavily search successful | query='%s' | results=%s | duration=%sms",
                clean_query,
                len(normalized),
                duration_ms,
            )
            return normalized

        except tavily_errors.InvalidAPIKeyError as exc:
            self._record_failure()
            logger.error("Tavily authentication failed: %s", exc)
            raise SearchAuthError(f"Tavily API key is invalid or unauthorized: {exc}", provider="tavily", query=clean_query) from exc

        except tavily_errors.UsageLimitExceededError as exc:
            self._record_failure()
            logger.error("Tavily rate or usage limit exceeded: %s", exc)
            raise SearchRateLimitError(f"Tavily quota or rate limit exceeded: {exc}", provider="tavily", query=clean_query) from exc

        except tavily_errors.TimeoutError as exc:
            self._record_failure()
            logger.error("Tavily search timed out: %s", exc)
            raise SearchTimeoutError(f"Tavily search timed out for query '{clean_query}': {exc}", provider="tavily", query=clean_query) from exc

        except tavily_errors.BadRequestError as exc:
            self._record_failure()
            logger.error("Tavily rejected bad request: %s", exc)
            raise InvalidQueryError(f"Tavily rejected request: {exc}", provider="tavily", query=clean_query) from exc

        except (EmptySearchResultsError, InvalidQueryError, SearchAuthError, SearchRateLimitError, SearchTimeoutError):
            # Re-raise already typed exceptions
            raise

        except Exception as exc:
            self._record_failure()
            logger.exception("Unexpected Tavily search error: %s", exc)
            raise WebSearchError(f"Tavily search failed for '{clean_query}': {exc}", provider="tavily", query=clean_query) from exc

    def _record_failure(self):
        with self._lock:
            self.failed_requests += 1
            self.last_search_status = "failed"

    def get_stats(self) -> Dict[str, Any]:
        """Return diagnostic metrics for UI and telemetry."""
        with self._lock:
            return {
                "provider": "tavily",
                "connected": self.is_connected(),
                "search_requests": self.search_requests,
                "failed_requests": self.failed_requests,
                "total_results_returned": self.total_results_returned,
                "last_response_time_ms": self.last_response_time_ms,
                "last_status": self.last_search_status,
                "api_usage": self.api_usage_data,
            }


# Global singleton client instance
tavily_search_client = TavilySearchClient()
