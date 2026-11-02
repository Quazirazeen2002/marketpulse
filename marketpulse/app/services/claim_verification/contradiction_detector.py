import re
import uuid
from typing import List, Dict, Optional, Any
from app.schemas import ResearchClaim, EvidenceRecord, ContradictionRecord


CONTRADICTION_PATTERNS = [
    (r"\bfree delivery\b|\bfree shipping\b", r"\bdelivery (?:charges?|fees?)\b|\bshipping (?:charges?|fees?)\b"),
    (r"\bgrowing\b|\bincreasing\b|\bsurging\b", r"\bdeclining\b|\bshrinking\b|\bslump\b"),
    (r"\bmarket leader\b", r"\blagging behind\b|\bstruggling\b"),
    (r"\bprofitable\b", r"\blosses\b|\bunprofitable\b"),
]


def detect_contradictions(
    claims: List[Any],
    evidence_records: Optional[List[Any]] = None,
    evidence: Optional[List[Any]] = None,
) -> List[ContradictionRecord]:
    """
    Detect explicit contradictions and conflicting factual statements across claims and evidence.
    """
    contradictions: List[ContradictionRecord] = []
    ev_list = evidence_records if evidence_records is not None else (evidence or [])

    # 1. Compare pairwise claims
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            claim_a = claims[i]
            claim_b = claims[j]

            text_a = getattr(claim_a, "claim_text", "") or (claim_a.get("claim_text", "") if isinstance(claim_a, dict) else "")
            text_b = getattr(claim_b, "claim_text", "") or (claim_b.get("claim_text", "") if isinstance(claim_b, dict) else "")
            text_a = text_a.lower()
            text_b = text_b.lower()

            cid_a = getattr(claim_a, "claim_id", "") or (claim_a.get("claim_id", "") if isinstance(claim_a, dict) else "")
            cid_b = getattr(claim_b, "claim_id", "") or (claim_b.get("claim_id", "") if isinstance(claim_b, dict) else "")
            agent_a = getattr(claim_a, "agent_name", "Specialist A") or (claim_a.get("agent_name", "Specialist A") if isinstance(claim_a, dict) else "Specialist A")
            agent_b = getattr(claim_b, "agent_name", "Specialist B") or (claim_b.get("agent_name", "Specialist B") if isinstance(claim_b, dict) else "Specialist B")

            # Pattern check
            for pos_pat, neg_pat in CONTRADICTION_PATTERNS:
                has_pos_a = bool(re.search(pos_pat, text_a))
                has_neg_b = bool(re.search(neg_pat, text_b))
                has_pos_b = bool(re.search(pos_pat, text_b))
                has_neg_a = bool(re.search(neg_pat, text_a))

                if (has_pos_a and has_neg_b) or (has_pos_b and has_neg_a):
                    cid = f"CONTR-{uuid.uuid4().hex[:6].upper()}"
                    sup_ev_a = getattr(claim_a, "supporting_evidence_ids", []) or (claim_a.get("supporting_evidence_ids", []) if isinstance(claim_a, dict) else [])
                    sup_ev_b = getattr(claim_b, "supporting_evidence_ids", []) or (claim_b.get("supporting_evidence_ids", []) if isinstance(claim_b, dict) else [])

                    contradictions.append(
                        ContradictionRecord(
                            contradiction_id=cid,
                            topic="Commercial Operations & Trends",
                            claim_a_id=cid_a,
                            claim_a_text=getattr(claim_a, "claim_text", text_a),
                            evidence_a_ids=sup_ev_a,
                            claim_b_id=cid_b,
                            claim_b_text=getattr(claim_b, "claim_text", text_b),
                            evidence_b_ids=sup_ev_b,
                            conflict_summary=f"Contradictory findings detected between '{agent_a}' and '{agent_b}'.",
                            resolution_status="unresolved",
                        )
                    )
                    # Link contradicting IDs if object attributes exist
                    if hasattr(claim_a, "contradicting_evidence_ids"):
                        claim_a.contradicting_evidence_ids.extend(sup_ev_b)
                    if hasattr(claim_b, "contradicting_evidence_ids"):
                        claim_b.contradicting_evidence_ids.extend(sup_ev_a)

    return contradictions


class ContradictionDetector:
    """Class wrapper for contradiction detection."""

    def detect(self, claims: List[Any], evidence_records: Optional[List[Any]] = None) -> List[ContradictionRecord]:
        return detect_contradictions(claims, evidence_records=evidence_records)
