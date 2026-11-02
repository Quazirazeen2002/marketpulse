import pytest
from app.schemas import (
    ResearchRequest,
    ResearchQuestion,
    ResearchPlan,
    SourceDocument,
    SourceQualityAssessment,
    EvidenceRecord,
    EvidenceGroup,
    ResearchClaim,
    ClaimVerification,
    ContradictionRecord,
    BusinessOpportunity,
    StrategicRecommendation,
    SpecialistReport,
    ExecutiveReport,
    ResearchQualityAssessment,
    ExecutionEvent,
    ExecutionStatus,
    ResearchQuality,
    VerificationStatus,
    SourceAcquisitionStatus,
    ClaimStatus,
    ClaimType,
    EventType,
)


def test_research_request_validation():
    req = ResearchRequest(
        objective="Analyze fashion e-commerce in Bangladesh",
        industry="Fashion & Retail",
        geography="Bangladesh",
    )
    assert req.objective == "Analyze fashion e-commerce in Bangladesh"
    assert req.industry == "Fashion & Retail"
    assert req.geography == "Bangladesh"
    assert req.max_search_queries_per_agent == 2


def test_source_document_status_enums():
    doc = SourceDocument(
        source_id="src_001",
        url="https://example.com/article",
        title="Market Overview",
        publisher="example.com",
        extraction_status=SourceAcquisitionStatus.RETRIEVED_FULL_TEXT,
        extracted_text="Full text content of the article...",
    )
    assert doc.extraction_status == SourceAcquisitionStatus.RETRIEVED_FULL_TEXT
    assert doc.is_canonical is True


def test_source_quality_assessment_bounds():
    qa = SourceQualityAssessment(
        source_id="src_001",
        credibility_score=85.0,
        relevance_score=90.0,
        freshness_score=80.0,
        completeness_score=75.0,
        specificity_score=70.0,
        composite_score=81.0,
        scoring_rationale="High quality authoritative source.",
    )
    assert qa.composite_score == 81.0

    # Bounds validation
    with pytest.raises(Exception):
        SourceQualityAssessment(
            source_id="src_bad",
            credibility_score=150.0,  # exceeds 100
            relevance_score=50.0,
            freshness_score=50.0,
            completeness_score=50.0,
            specificity_score=50.0,
            composite_score=50.0,
        )


def test_research_claim_and_verification():
    claim = ResearchClaim(
        claim_id="CLM-001",
        agent_name="Competitor Intelligence Analyst",
        claim_text="Daraz offers nationwide home delivery across Bangladesh.",
        claim_type=ClaimType.COMPETITOR_STRATEGY,
        supporting_evidence_ids=["EV-001", "EV-002"],
        verification_status=ClaimStatus.SUPPORTED,
        confidence_score=0.88,
        verification_rationale="Corroborated by 2 independent sources.",
    )
    assert claim.verification_status == ClaimStatus.SUPPORTED
    assert len(claim.supporting_evidence_ids) == 2
    assert claim.confidence_score == 0.88


def test_contradiction_record():
    con = ContradictionRecord(
        contradiction_id="CON-001",
        topic="Delivery Fees",
        claim_a_id="CLM-001",
        claim_a_text="Company A offers free delivery on all orders.",
        claim_b_id="CLM-002",
        claim_b_text="Company A charges 60 BDT delivery fee outside Dhaka.",
        conflict_summary="Conflicting delivery pricing policies reported.",
    )
    assert con.resolution_status == "unresolved"
    assert "delivery" in con.conflict_summary.lower()


def test_executive_report_serialization():
    rep = ExecutiveReport(
        research_id="run_12345",
        objective="Analyze fintech landscape",
        industry="Fintech",
        geography="Bangladesh",
        executive_summary="Summary of findings...",
        market_intelligence="Market details...",
        competitor_intelligence="Competitor details...",
        customer_intelligence="Customer details...",
        execution_status=ExecutionStatus.COMPLETED,
        research_quality=ResearchQuality.STRONG,
        verification_status=VerificationStatus.VERIFIED,
    )
    dump = rep.model_dump()
    assert dump["research_id"] == "run_12345"
    assert dump["research_quality"] == "strong"
    assert dump["verification_status"] == "verified"
