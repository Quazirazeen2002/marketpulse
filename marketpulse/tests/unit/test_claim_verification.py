import pytest
from app.schemas import ResearchClaim, EvidenceRecord, ClaimStatus, ClaimType
from app.services.claim_verification.contradiction_detector import detect_contradictions
from app.services.claim_verification.claim_verifier import verify_claims_against_evidence
from app.services.claim_verification.citation_validator import validate_citations_and_traceability


def test_scenario_5_contradictory_evidence_detection():
    """Test 5: Conflicting statements on delivery policies are detected as contradictions."""
    claim_a = ResearchClaim(
        claim_id="CLM-FREE-DEL",
        agent_name="Competitor Analyst",
        claim_text="Daraz provides free shipping and delivery on all orders nationwide.",
        claim_type=ClaimType.COMPETITOR_STRATEGY,
        supporting_evidence_ids=["EV-FREE"],
    )

    claim_b = ResearchClaim(
        claim_id="CLM-FEE-DEL",
        agent_name="Competitor Analyst",
        claim_text="Daraz charges delivery fee and shipping cost for orders outside Dhaka.",
        claim_type=ClaimType.COMPETITOR_STRATEGY,
        supporting_evidence_ids=["EV-FEE"],
    )

    contradictions = detect_contradictions([claim_a, claim_b])

    assert len(contradictions) >= 1
    con = contradictions[0]
    assert con.claim_a_id in ("CLM-FREE-DEL", "CLM-FEE-DEL")
    assert con.claim_b_id in ("CLM-FREE-DEL", "CLM-FEE-DEL")
    assert con.resolution_status == "unresolved"


def test_scenario_6_unsupported_claim_classified_unverified():
    """Test 6: Specialist claim with no supporting evidence is classified as unverified hypothesis."""
    unsupported_claim = ResearchClaim(
        claim_id="CLM-NO-EV",
        agent_name="Market Analyst",
        claim_text="Fabrilife captured 35% of the nationwide polo shirt market share in 2026.",
        claim_type=ClaimType.MARKET_STRUCTURE,
        supporting_evidence_ids=[],  # No evidence
        verification_status=ClaimStatus.UNVERIFIED,
    )

    validated = validate_citations_and_traceability([unsupported_claim], evidence_registry=[])

    assert len(validated) == 1
    assert validated[0].verification_status in (ClaimStatus.UNVERIFIED, ClaimStatus.INSUFFICIENT_EVIDENCE)
    assert validated[0].is_hypothesis is True
    assert "hypothes" in validated[0].verification_rationale.lower() or "lacks" in validated[0].verification_rationale.lower()
