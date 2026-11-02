import pytest
from app.schemas import SourceDocument, SourceAcquisitionStatus
from app.services.evidence_intelligence.source_evaluator import evaluate_source_quality


def test_source_quality_five_dimensions():
    doc = SourceDocument(
        source_id="src_high_qual",
        url="https://worldbank.org/reports/bangladesh-retail",
        title="Bangladesh Retail Economic Report 2026",
        publisher="worldbank.org",
        publication_date="2026-02-10",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text="The retail industry in Bangladesh expanded by 8.4% in 2025, reaching BDT 450 billion in total sales with 40% urban penetration.",
    )

    qa = evaluate_source_quality(
        source=doc,
        objective="Analyze retail market growth in Bangladesh",
        industry="Retail",
        geography="Bangladesh",
    )

    assert qa.composite_score >= 70.0
    assert qa.credibility_score >= 80.0
    assert qa.relevance_score >= 80.0
    assert qa.specificity_score >= 70.0
    assert "Composite Score" in qa.scoring_rationale


def test_scenario_7_historical_vs_current_freshness():
    """Test 7: Historical vs current data is properly penalized for time-sensitive pricing/campaign topics."""
    old_doc = SourceDocument(
        source_id="src_old",
        url="https://dailynews.com/archive-2018",
        title="Daraz Flash Sale 2018",
        publisher="dailynews.com",
        publication_date="2018-05-12",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text="Daraz offers 10% discount on summer shirts during 2018 campaign.",
    )

    current_doc = SourceDocument(
        source_id="src_new",
        url="https://dailynews.com/campaign-2026",
        title="Daraz Seasonal Promotion 2026",
        publisher="dailynews.com",
        publication_date="2026-03-01",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text="Daraz launches 2026 seasonal promotional campaign with 20% discount vouchers.",
    )

    qa_old = evaluate_source_quality(
        source=old_doc,
        objective="Investigate competitor promotional pricing in Bangladesh",
        industry="Fashion",
        geography="Bangladesh",
    )

    qa_new = evaluate_source_quality(
        source=current_doc,
        objective="Investigate competitor promotional pricing in Bangladesh",
        industry="Fashion",
        geography="Bangladesh",
    )

    # Current pricing source should score higher in freshness than 2018 archive
    assert qa_new.freshness_score > qa_old.freshness_score
    assert old_doc.publication_date == "2018-05-12"
    assert current_doc.publication_date == "2026-03-01"
