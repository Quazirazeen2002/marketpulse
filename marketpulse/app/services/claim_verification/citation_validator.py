from typing import List, Dict, Set, Tuple, Any, Optional
from app.schemas import ResearchClaim, EvidenceRecord, SourceDocument, ClaimStatus


def validate_citations_and_traceability(
    claims: List[Any],
    evidence_records: Optional[List[Any]] = None,
    sources: Optional[List[Any]] = None,
    evidence_registry: Optional[List[Any]] = None,
    evidence: Optional[List[Any]] = None,
    return_metrics: bool = False,
) -> Any:
    """
    Validate that every claim has authentic, traceable citations to actual evidence and sources.
    Relabels unsupported claims as hypotheses and tracks citation integrity metrics.
    """
    ev_list = evidence_records if evidence_records is not None else (evidence_registry or evidence or [])
    src_list = sources or []

    valid_evidence_ids: Set[str] = {
        getattr(e, "evidence_id", "") or (e.get("evidence_id", "") if isinstance(e, dict) else "")
        for e in ev_list
    }
    evidence_map: Dict[str, Any] = {
        (getattr(e, "evidence_id", "") or (e.get("evidence_id", "") if isinstance(e, dict) else "")): e
        for e in ev_list
    }

    metrics = {
        "total_claims": len(claims),
        "traceable_claims": 0,
        "untraceable_claims": 0,
        "relabeled_hypotheses": 0,
        "snippet_only_citations": 0,
    }

    validated_claims: List[ResearchClaim] = []

    for c in claims:
        claim = c if isinstance(c, ResearchClaim) else ResearchClaim(**c)
        # Check that linked evidence IDs actually exist in stored records
        traceable_ev_ids = [eid for eid in claim.supporting_evidence_ids if eid in valid_evidence_ids]

        if not traceable_ev_ids:
            # If a factual claim has no valid evidence, mark as hypothesis / unverified
            metrics["untraceable_claims"] += 1
            metrics["relabeled_hypotheses"] += 1
            claim.is_hypothesis = True
            claim.verification_status = ClaimStatus.UNVERIFIED
            claim.supporting_evidence_ids = []
            claim.verification_rationale = "No verifiable evidence records found; classified as an analytical hypothesis."
        else:
            metrics["traceable_claims"] += 1
            claim.supporting_evidence_ids = traceable_ev_ids

            # Check if any evidence is snippet only
            has_snippet = any(
                getattr(evidence_map[eid], "extraction_quality", "") == "snippet_derived"
                or (isinstance(evidence_map[eid], dict) and evidence_map[eid].get("extraction_quality") == "snippet_derived")
                for eid in traceable_ev_ids
                if eid in evidence_map
            )
            if has_snippet:
                metrics["snippet_only_citations"] += 1

        validated_claims.append(claim)

    if return_metrics:
        return validated_claims, metrics
    return validated_claims


class CitationValidator:
    """Class wrapper for citation validation and traceability."""

    def validate(
        self,
        claims: List[Any],
        evidence_records: Optional[List[Any]] = None,
        sources: Optional[List[Any]] = None,
    ) -> List[ResearchClaim]:
        return validate_citations_and_traceability(
            claims=claims,
            evidence_records=evidence_records,
            sources=sources,
        )
