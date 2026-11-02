import pytest
from app.schemas import SourceDocument, SourceAcquisitionStatus
from app.services.evidence_intelligence.deduplication import cluster_and_deduplicate_sources, cluster_sources_and_evidence


def test_scenario_4_duplicate_articles_clustering():
    """Test 4: Identical or near-identical articles across different URLs are clustered into one group."""
    article_text = (
        "Dhaka, March 2026: The Bangladesh e-commerce sector witnessed record transaction volumes "
        "following the introduction of nationwide express logistics partnerships. Local retailers reported "
        "an average 25% uplift in fashion category orders."
    )

    doc_a = SourceDocument(
        source_id="src_site_a",
        url="https://news-hub-a.com/retail-express",
        title="Bangladesh E-commerce Surges with Express Logistics",
        publisher="news-hub-a.com",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text=article_text,
        content_hash="hash_identical_1234",
    )

    doc_b = SourceDocument(
        source_id="src_syndicated_b",
        url="https://syndicated-times.com/retail-express-reprint",
        title="Bangladesh E-commerce Surges with Express Logistics (Reprint)",
        publisher="syndicated-times.com",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text=article_text + " Syndicated via Asian News wire.",
        content_hash="hash_identical_1234",
    )

    clustered, groups = cluster_and_deduplicate_sources([doc_a, doc_b])

    assert len(groups) == 1
    assert groups[0].canonical_source_id in ("src_site_a", "src_syndicated_b")
    # One document should be canonical, the other duplicate
    canonical_docs = [d for d in clustered if d.is_canonical]
    duplicate_docs = [d for d in clustered if not d.is_canonical]

    assert len(canonical_docs) == 1
    assert len(duplicate_docs) == 1
    assert duplicate_docs[0].duplicate_group_id == canonical_docs[0].duplicate_group_id
