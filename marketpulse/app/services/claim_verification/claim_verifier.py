import uuid
from typing import List, Dict, Tuple, Optional, Any
from app.schemas import ResearchClaim, EvidenceRecord, ClaimVerification, ClaimStatus, SourceQualityAssessment
from .confidence_calculator import calculate_claim_confidence


def verify_claims_against_evidence(
    claims: List[ResearchClaim],
    evidence_records: Optional[List[EvidenceRecord]] = None,
    source_quality_map: Optional[Dict[str, SourceQualityAssessment]] = None,
    evidence: Optional[List[EvidenceRecord]] = None,
    source_qualities: Optional[Dict[str, SourceQualityAssessment]] = None,
    **kwargs: Any,
) -> Tuple[List[ResearchClaim], List[ClaimVerification]]:
    """
    Verify claims against empirical evidence records.
    Assigns strict verification statuses and confidence calculations.
    """
    records = evidence_records if evidence_records is not None else (evidence or [])
    sq_map = source_quality_map if source_quality_map is not None else (source_qualities or {})

    evidence_map: Dict[str, Any] = {}
    for e in records:
        eid = getattr(e, "evidence_id", None) or (e.get("evidence_id") if isinstance(e, dict) else None)
        if eid:
            evidence_map[eid] = e


    verified_claims: List[ResearchClaim] = []
    verifications: List[ClaimVerification] = []

    for claim in claims:
        sup_evidence = [evidence_map[eid] for eid in claim.supporting_evidence_ids if eid in evidence_map]
        contra_evidence = [evidence_map[eid] for eid in claim.contradicting_evidence_ids if eid in evidence_map]

        conf_score, conf_rationale = calculate_claim_confidence(
            claim_text=claim.claim_text,
            supporting_evidence=sup_evidence,
            contradicting_evidence=contra_evidence,
            source_quality_map=sq_map,
            is_hypothesis=claim.is_hypothesis,
        )

        # Count independent domains / groups
        unique_publishers = {
            (getattr(e, "publisher", None) or (e.get("publisher") if isinstance(e, dict) else "") or "").lower()
            for e in sup_evidence
        }
        unique_publishers.discard("")
        independent_count = len(unique_publishers) or (1 if sup_evidence else 0)


        # Determine Status
        if contra_evidence:
            status = ClaimStatus.CONTRADICTED
        elif not sup_evidence:
            status = ClaimStatus.UNVERIFIED
        elif independent_count >= 2 and conf_score >= 0.72:
            status = ClaimStatus.SUPPORTED
        elif sup_evidence and conf_score >= 0.45:
            status = ClaimStatus.PARTIALLY_SUPPORTED
        else:
            status = ClaimStatus.INSUFFICIENT_EVIDENCE

        claim.verification_status = status
        claim.confidence_score = conf_score
        claim.verification_rationale = conf_rationale

        verified_claims.append(claim)

        vid = f"VERIF-{uuid.uuid4().hex[:6].upper()}"
        verifications.append(
            ClaimVerification(
                verification_id=vid,
                claim_id=claim.claim_id,
                status=status,
                supporting_sources_count=len(sup_evidence),
                contradicting_sources_count=len(contra_evidence),
                independent_sources_count=independent_count,
                confidence_score=conf_score,
                confidence_rationale=conf_rationale,
            )
        )

    return verified_claims, verifications
