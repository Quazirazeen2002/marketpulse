import pytest
import fitz
from app.services.source_acquisition.pdf_extractor import extract_pdf_content


def create_in_memory_pdf() -> bytes:
    """Generate a clean 2-page research PDF in-memory for testing."""
    doc = fitz.open()

    page1 = doc.new_page()
    page1.insert_text(
        fitz.Point(50, 72),
        "Market Research Report: Bangladesh Retail Trends\n"
        "Page 1 Overview: Online retail penetration stands at 4.5% nationwide.\n"
        "Daraz accounts for an estimated 40% of marketplace traffic.",
    )

    page2 = doc.new_page()
    page2.insert_text(
        fitz.Point(50, 72),
        "Page 2 Competitor Analysis: Traditional apparel brands have launched omnichannel portals.\n"
        "Delivery fee variations remain a primary driver of customer drop-off.",
    )

    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


def test_pdf_extraction_page_numbers_and_content():
    pdf_bytes = create_in_memory_pdf()
    full_text, pages_dict, meta, status = extract_pdf_content(pdf_bytes, max_pages=5)

    assert status == "retrieved_full_text"
    assert meta["page_count"] == 2
    assert 1 in pages_dict
    assert 2 in pages_dict
    assert "Online retail penetration stands at 4.5%" in pages_dict[1]
    assert "Traditional apparel brands have launched omnichannel" in pages_dict[2]
    assert "[Page 1]" in full_text
    assert "[Page 2]" in full_text


def test_pdf_extraction_page_limit():
    pdf_bytes = create_in_memory_pdf()
    full_text, pages_dict, meta, status = extract_pdf_content(pdf_bytes, max_pages=1)
    assert len(pages_dict) == 1
    assert 1 in pages_dict
    assert 2 not in pages_dict
