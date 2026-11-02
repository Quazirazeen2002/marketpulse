import pytest
from unittest.mock import patch
from app.schemas import SourceAcquisitionStatus
from app.services.source_acquisition.engine import acquire_source


FULL_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Bangladesh Retail Boom 2026</title></head>
<body>
    <article>
        <h1>Retail Boom in Bangladesh</h1>
        <p>Consumer demand for modern apparel has grown substantially over the last two fiscal quarters across major urban centers including Dhaka, Chittagong, and Sylhet. Leading domestic manufacturers and digital fashion brands report accelerating omnichannel adoption among young urban shoppers.</p>
        <p>According to comprehensive retail commerce surveys, marketplace transaction volumes increased by over 28% year-on-year, propelled by faster nationwide delivery networks and widespread integration of mobile financial payment gateways.</p>
        <p>Market analysts project sustained double-digit expansion throughout 2026, as traditional high-street garment retailers expand their online direct-to-consumer portals to compete with regional digital incumbents.</p>
    </article>
</body>
</html>
"""


def test_scenario_1_full_article_retrieval():
    """Test 1: Search result containing an accessible article retrieves full text."""
    with patch("app.services.source_acquisition.engine.fetch_url") as mock_fetch:
        mock_fetch.return_value = (FULL_ARTICLE_HTML.encode("utf-8"), "text/html", 200, None)

        doc = acquire_source(
            url="https://businessnews.com/fashion-boom",
            fallback_title="Retail Boom in Bangladesh",
            fallback_snippet="Consumer demand for apparel has grown...",
        )

        assert doc.extraction_status in (
            SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
            SourceAcquisitionStatus.RETRIEVED_PARTIAL,
        )
        assert "Consumer demand for modern apparel" in doc.extracted_text
        assert doc.content_hash != ""
        assert doc.publisher == "businessnews.com"


def test_scenario_2_snippet_only_on_inaccessible():
    """Test 2: Inaccessible URL retains search excerpt as snippet-only without fabricating text."""
    with patch("app.services.source_acquisition.engine.fetch_url") as mock_fetch:
        mock_fetch.return_value = (None, "text/html", 403, "HTTP 403 Forbidden")

        fallback_snippet = "Leading e-commerce platforms offer seasonal discounts."
        doc = acquire_source(
            url="https://paywalled-journal.com/study",
            fallback_title="E-commerce Analysis",
            fallback_snippet=fallback_snippet,
        )

        assert doc.extraction_status == SourceAcquisitionStatus.SNIPPET_ONLY
        assert doc.extracted_text == fallback_snippet
        assert "paywalled-journal.com" in doc.url
        assert doc.error_message == "HTTP 403 Forbidden"


def test_invalid_url_handling():
    doc = acquire_source(url="not_a_valid_url", fallback_title="Invalid URL")
    assert doc.extraction_status == SourceAcquisitionStatus.INACCESSIBLE
