import pytest
from app.schemas import SourceDocument, SourceAcquisitionStatus
from app.services.evidence_intelligence.evidence_extractor import extract_evidence_from_source


def test_scenario_3_pdf_evidence_extraction_with_page_numbers():
    """Test 3: Evidence extracted from PDF retains page number and provenance."""
    pdf_text = (
        "--- [Page 1] ---\n\n"
        "Executive Summary: Bangladesh retail sector online share stands at 4.5% nationwide according to official industry statistics. Urban penetration across metropolitan zones continues to expand.\n\n"
        "--- [Page 2] ---\n\n"
        "Competitor Landscape: Daraz holds 42% market share in general merchandise e-commerce, while vertical fashion platforms have increased regional distribution networks."
    )

    doc = SourceDocument(
        source_id="src_pdf_report",
        url="https://industry-analytics.com/bangladesh-2026.pdf",
        title="Bangladesh E-commerce Industry Report",
        publisher="industry-analytics.com",
        content_type="application/pdf",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text=pdf_text,
    )

    records = extract_evidence_from_source(doc, max_excerpts=4)
    assert len(records) >= 2

    # Check page references
    page_numbers = {r.page_number for r in records if r.page_number is not None}
    assert 1 in page_numbers or 2 in page_numbers
    assert any("4.5%" in r.exact_excerpt or "42%" in r.exact_excerpt for r in records)


def test_html_article_evidence_extraction():
    article_text = (
        "Section 1: Market Dynamics\n\n"
        "Online fashion sales grew 32% year-over-year in Bangladesh, led by youth apparel demand across urban areas.\n\n"
        "Section 2: Payment Infrastructure\n\n"
        "Cash on delivery accounts for over 70% of transactions, though bKash and Nagad mobile wallets are growing steadily."
    )

    doc = SourceDocument(
        source_id="src_html_report",
        url="https://techbangla.com/fintech-retail",
        title="Payment Shifts in Bangladesh Retail",
        publisher="techbangla.com",
        content_type="text/html",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text=article_text,
    )

    records = extract_evidence_from_source(doc, max_excerpts=3)
    assert len(records) >= 1
    assert any("32%" in r.exact_excerpt or "70%" in r.exact_excerpt for r in records)
    assert records[0].source_id == "src_html_report"
    assert records[0].source_url == "https://techbangla.com/fintech-retail"
