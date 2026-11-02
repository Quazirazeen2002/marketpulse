from typing import List, Dict, Tuple, Any
from app.schemas import EvidenceRecord, SourceQualityAssessment


def _get_val(obj: Any, field: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(field, default)
    return getattr(obj, field, default)


def calculate_claim_confidence(
    claim_text: str,
    supporting_evidence: List[EvidenceRecord],
    contradicting_evidence: List[EvidenceRecord],
    source_quality_map: Dict[str, SourceQualityAssessment] = None,
    is_hypothesis: bool = False,
) -> Tuple[float, str]:
    """
    Calculate a transparent, rule-based confidence assessment (0.0 - 1.0).
    Factors:
    - Number of independent supporting sources (unique domains / groups)
    - Quality of supporting sources
    - Directness of excerpt overlap
    - Contradictory evidence penalty
    - Snippet-only vs full-text extraction quality
    """
    source_quality_map = source_quality_map or {}
    rationale_parts = []

    if is_hypothesis:
        return 0.35, "Classified as an analytical hypothesis; requires empirical validation."

    if not supporting_evidence:
        return 0.15, "Unsupported claim: no linked empirical evidence records found."

    # 1. Independent Source Corroboration
    unique_domains = set()
    unique_groups = set()
    snippet_count = 0

    for ev in supporting_evidence:
        pub = _get_val(ev, "publisher")
        if pub:
            unique_domains.add(str(pub).lower())
        grp = _get_val(ev, "duplicate_group_id")
        if grp:
            unique_groups.add(str(grp))
        if _get_val(ev, "extraction_quality") == "snippet_derived":
            snippet_count += 1

    independent_sources = max(len(unique_domains), len(unique_groups), 1)

    if independent_sources >= 3:
        base_score = 0.88
        rationale_parts.append(f"Strong independent corroboration across {independent_sources} distinct sources/domains")
    elif independent_sources == 2:
        base_score = 0.78
        rationale_parts.append("Corroborated by 2 independent sources")
    else:
        base_score = 0.62
        rationale_parts.append("Single source reliance; claims should be interpreted narrowly")

    # 2. Source Quality Adjustment
    avg_quality = 70.0
    qualities = []
    for ev in supporting_evidence:
        sid = _get_val(ev, "source_id")
        if sid and sid in source_quality_map:
            qa = source_quality_map[sid]
            comp = getattr(qa, "composite_score", None) or (qa.get("composite_score") if isinstance(qa, dict) else None)
            if comp is not None:
                qualities.append(float(comp))
    if qualities:
        avg_quality = sum(qualities) / len(qualities)
        if avg_quality >= 80.0:
            base_score += 0.08
            rationale_parts.append(f"high-quality supporting sources (avg: {avg_quality:.0f}/100)")
        elif avg_quality < 55.0:
            base_score -= 0.12
            rationale_parts.append(f"low-quality supporting sources (avg: {avg_quality:.0f}/100)")


    # 3. Snippet-Only Penalty
    if snippet_count == len(supporting_evidence):
        base_score -= 0.18
        rationale_parts.append("penalized: based entirely on brief search engine snippets")
    elif snippet_count > 0:
        base_score -= 0.06
        rationale_parts.append("partially relies on search snippets")

    # 4. Contradiction Penalty
    if contradicting_evidence:
        base_score -= 0.35
        rationale_parts.append(f"severe penalty: {len(contradicting_evidence)} conflicting evidence record(s) detected")

    final_score = round(max(0.10, min(0.96, base_score)), 2)
    return final_score, "; ".join(rationale_parts)
