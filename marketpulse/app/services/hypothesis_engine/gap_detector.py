"""
Research Gap Detector for Autonomous Opportunity Discovery.
Scans multi-agent findings, claims, and customer friction signals to identify
unverified assertions, conflicting evidence, or crucial missing business data.
"""

from typing import List, Dict, Any, Optional
from app.schemas.strategic import ResearchHypothesis


def detect_research_gaps(
    findings_by_agent: Optional[Dict[str, Any]] = None,
    claims: Optional[List[Dict[str, Any]]] = None,
    contradictions: Optional[List[Dict[str, Any]]] = None,
    unverified_claims: Optional[List[str]] = None,
    specialist_gaps: Optional[List[str]] = None,
) -> List[str]:
    """
    Detect missing commercial information, unverified hypotheses,
    and ambiguous customer data across agent outputs.
    """
    gaps: List[str] = []
    findings_by_agent = findings_by_agent or {}
    claims = claims or []
    contradictions = contradictions or []

    # 1. Inspect contradictions
    for c in contradictions:
        if isinstance(c, dict):
            conflict = c.get("conflict_summary") or f"Conflict between {c.get('claim_a_id')} and {c.get('claim_b_id')}"
            gaps.append(f"Contradictory evidence requiring independent corroboration: {conflict}")
        elif isinstance(c, str):
            gaps.append(f"Contradictory evidence: {c}")

    # 2. Inspect unverified claims
    for clm in claims:
        if isinstance(clm, dict):
            status = clm.get("verification_status")
            if status in ("unverified", "insufficient_evidence", "disputed"):
                text = clm.get("claim_text", "")
                if len(text) > 20:
                    gaps.append(f"Unverified commercial assertion: '{text[:90]}...'")

    if unverified_claims:
        for u in unverified_claims:
            gaps.append(f"Unverified assertion: {u}")

    if specialist_gaps:
        for s in specialist_gaps:
            gaps.append(s)

    # 3. Inspect agent-reported research gaps
    for agent_name, rep in findings_by_agent.items():
        if isinstance(rep, dict):
            agent_gaps = rep.get("research_gaps", []) or rep.get("missing_information", [])
            for g in agent_gaps:
                if g and g not in gaps:
                    gaps.append(f"[{agent_name}] {g}")

    # Deduplicate and limit to high-priority gaps
    unique_gaps = list(dict.fromkeys(gaps))
    return unique_gaps[:10]
