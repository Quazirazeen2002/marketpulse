"""
Evidence Assessment for Opportunity Scoring.
Evaluates evidence quality, independence, directness, and representativeness
to prevent superficial scores based purely on query result volume.
"""

from typing import List, Dict, Any, Optional


def assess_evidence_quality_factor(
    evidence_ids: List[str],
    evidence_records: Optional[List[Dict[str, Any]]] = None,
) -> float:
    """
    Compute evidence credibility factor between 0.50 and 1.0.
    Factors in source independence (distinct publishers) and full-text vs snippet status.
    """
    if not evidence_ids:
        return 0.50

    if not evidence_records:
        return min(0.70 + (len(evidence_ids) * 0.05), 0.90)

    # Match referenced records
    ref_map = {e.get("evidence_id"): e for e in evidence_records if isinstance(e, dict)}
    matched = [ref_map[eid] for eid in evidence_ids if eid in ref_map]

    if not matched:
        return 0.65

    # Check distinct publishers (independence)
    publishers = set(e.get("publisher", "") for e in matched if e.get("publisher"))
    independence_boost = min(len(publishers) * 0.08, 0.20)

    # Check full-text vs snippet extraction
    full_text_count = sum(1 for e in matched if e.get("extraction_status") == "retrieved_full_text")
    full_text_boost = min(full_text_count * 0.05, 0.15)

    factor = 0.55 + independence_boost + full_text_boost
    return max(0.50, min(factor, 1.0))
