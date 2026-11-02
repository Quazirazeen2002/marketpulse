import pytest
from app.schemas import ResearchClaim, EvidenceRecord, ClaimStatus
from app.services.claim_verification.citation_validator import validate_citations_and_traceability


def test_citation_validation_valid_evidence():
    ev = EvidenceRecord(
        evidence_id="EV-REAL-001",
        source_id="src_01",
        source_url="https://verified.com/news",
        source_title="Verified News",
        exact_excerpt="Daraz runs 11.11 shopping mega campaigns annually.",
    )

    claim = ResearchClaim(
        claim_id="CLM-01",
        agent_name="Competitor Analyst",
        claim_text="Daraz operates annual 11.11 promotional campaigns.",
        supporting_evidence_ids=["EV-REAL-001"],
    )

    validated = validate_citations_and_traceability([claim], evidence_registry=[ev])
    assert len(validated) == 1
    assert "EV-REAL-001" in validated[0].supporting_evidence_ids


def test_citation_validation_phantom_evidence_reclassification():
    claim = ResearchClaim(
        claim_id="CLM-PHANTOM",
        agent_name="Competitor Analyst",
        claim_text="Competitor revenue reached $500 million in Q1.",
        supporting_evidence_ids=["EV-NON-EXISTENT"],
    )

    validated = validate_citations_and_traceability([claim], evidence_registry=[])
    assert len(validated) == 1
    assert "EV-NON-EXISTENT" not in validated[0].supporting_evidence_ids
    assert validated[0].is_hypothesis is True
