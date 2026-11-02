"""
Unit tests for TavilySearchClient and search_web wrapper.
Uses mocked Tavily SDK responses for deterministic testing without consuming API credits.
"""

from unittest.mock import MagicMock, patch
import pytest
from tavily import errors as tavily_errors

from app.services.web_search.client import TavilySearchClient
from app.services.web_search.search import search_web
from app.services.web_search.exceptions import (
    SearchAuthError,
    SearchRateLimitError,
    SearchTimeoutError,
    InvalidQueryError,
    EmptySearchResultsError,
)


def test_missing_api_key_raises_auth_error():
    client = TavilySearchClient(api_key="")
    with pytest.raises(SearchAuthError):
        client.search("test query")


def test_empty_query_raises_invalid_query_error():
    client = TavilySearchClient(api_key="tvly-test-key")
    with pytest.raises(InvalidQueryError):
        client.search("")


def test_successful_search_normalized():
    client = TavilySearchClient(api_key="tvly-mock-key")

    mock_sdk_client = MagicMock()
    mock_sdk_client.search.return_value = {
        "results": [
            {
                "title": "Chaldal Grocery Delivery Expands in Dhaka",
                "url": "https://www.thedailystar.net/business/chaldal-expansion",
                "content": "Chaldal has introduced 15-minute grocery deliveries in central Dhaka hubs.",
                "score": 0.94,
                "published_date": "2026-02-14",
            }
        ],
        "usage": {"credits": 1},
    }
    client._client = mock_sdk_client

    results = client.search("Chaldal expansion Dhaka", max_results=5)
    assert len(results) == 1
    assert results[0]["title"] == "Chaldal Grocery Delivery Expands in Dhaka"
    assert results[0]["publisher"] == "thedailystar.net"
    assert results[0]["search_provider"] == "tavily"
    assert results[0]["source_type"] == "tavily_search"
    assert results[0]["score"] == 0.94
    assert client.search_requests == 1
    assert client.failed_requests == 0


def test_empty_results_raises_empty_search_results_error():
    client = TavilySearchClient(api_key="tvly-mock-key")
    mock_sdk_client = MagicMock()
    mock_sdk_client.search.return_value = {"results": []}
    client._client = mock_sdk_client

    with pytest.raises(EmptySearchResultsError):
        client.search("obscure non-existent keyword 123456")

    assert client.failed_requests == 0  # 0 results is not a provider failure, but raises typed exception


def test_authentication_failure_maps_to_search_auth_error():
    client = TavilySearchClient(api_key="tvly-bad-key")
    mock_sdk_client = MagicMock()
    mock_sdk_client.search.side_effect = tavily_errors.InvalidAPIKeyError("Invalid API key provided")
    client._client = mock_sdk_client

    with pytest.raises(SearchAuthError):
        client.search("market trends")

    assert client.failed_requests == 1


def test_rate_limit_maps_to_search_rate_limit_error():
    client = TavilySearchClient(api_key="tvly-mock-key")
    mock_sdk_client = MagicMock()
    mock_sdk_client.search.side_effect = tavily_errors.UsageLimitExceededError("Plan limit exceeded")
    client._client = mock_sdk_client

    with pytest.raises(SearchRateLimitError):
        client.search("market trends")

    assert client.failed_requests == 1


def test_timeout_maps_to_search_timeout_error():
    client = TavilySearchClient(api_key="tvly-mock-key")
    mock_sdk_client = MagicMock()
    mock_sdk_client.search.side_effect = tavily_errors.TimeoutError("Request timed out")
    client._client = mock_sdk_client

    with pytest.raises(SearchTimeoutError):
        client.search("market trends")

    assert client.failed_requests == 1
