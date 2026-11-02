"""
Deterministic Opportunity Scoring Engine for MARKETPULSE Stage 2.
Implements the exact 6-dimensional weighted deterministic formula with transparent rationale,
evidence quality weighting, and separate risk adjustment.
"""

from typing import Dict, Any, List, Optional
from app.schemas.strategic import OpportunityScore
from app.services.opportunity_scoring.dimensions import DEFAULT_DIMENSION_WEIGHTS, validate_weights
from app.services.opportunity_scoring.evidence_assessment import assess_evidence_quality_factor
from app.services.opportunity_scoring.risk_adjustment import calculate_risk_penalty


def score_opportunity(
    opportunity: Dict[str, Any],
    risks: Optional[List[Dict[str, Any]]] = None,
    evidence_records: Optional[List[Dict[str, Any]]] = None,
    custom_weights: Optional[Dict[str, float]] = None,
) -> OpportunityScore:
    """
    Score a single business opportunity deterministically across 6 core dimensions.
    Returns OpportunityScore with both raw_score and risk_adjusted_score.
    """
    weights = custom_weights or DEFAULT_DIMENSION_WEIGHTS
    if not validate_weights(weights):
        weights = DEFAULT_DIMENSION_WEIGHTS

    opp_id = opportunity.get("opportunity_id", "OPP-001")
    evidence_ids = opportunity.get("supporting_evidence_ids", [])

    # Evaluate empirical evidence factor (0.50 - 1.0)
    ev_factor = assess_evidence_quality_factor(evidence_ids, evidence_records)

    # 1. Customer Demand (0-100)
    # Driven by evidence backing and specific pain point clarity
    demand_base = 65.0
    if len(opportunity.get("supporting_findings", [])) >= 2:
        demand_base += 15.0
    demand_score = min(100.0, round(demand_base * ev_factor, 1))

    # 2. Competitive Gap (0-100)
    # Evaluates competitor blind spots and incumbent weaknesses
    gap_base = 70.0
    if len(opportunity.get("relevant_competitors", [])) > 0:
        gap_base += 10.0
    gap_score = min(100.0, round(gap_base * (0.85 + (0.15 * ev_factor)), 1))

    # 3. Commercial Attractiveness (0-100)
    # Evaluates commercial model clarity and customer value proposition
    comm_base = 70.0
    if "subscription" in opportunity.get("commercial_model", "").lower() or "direct-to-consumer" in opportunity.get("commercial_model", "").lower():
        comm_base += 10.0
    comm_score = min(100.0, comm_base)

    # 4. Implementation Feasibility (0-100)
    # High barriers reduce feasibility score
    barriers = opportunity.get("potential_barriers", [])
    feas_base = max(40.0, 85.0 - (len(barriers) * 8.0))
    feas_score = min(100.0, feas_base)

    # 5. Market Growth Potential (0-100)
    growth_score = 75.0

    # 6. Strategic Differentiation (0-100)
    diff_base = 65.0
    if len(opportunity.get("competitive_differentiation", "")) > 30:
        diff_base += 15.0
    diff_score = min(100.0, diff_base)

    components = {
        "customer_demand": demand_score,
        "competitive_gap": gap_score,
        "commercial_attractiveness": comm_score,
        "implementation_feasibility": feas_score,
        "market_growth": growth_score,
        "strategic_differentiation": diff_score,
    }

    # Deterministic weighted calculation:
    raw_score = round(
        (components["customer_demand"] * weights["customer_demand"])
        + (components["competitive_gap"] * weights["competitive_gap"])
        + (components["commercial_attractiveness"] * weights["commercial_attractiveness"])
        + (components["implementation_feasibility"] * weights["implementation_feasibility"])
        + (components["market_growth"] * weights["market_growth"])
        + (components["strategic_differentiation"] * weights["strategic_differentiation"]),
        1,
    )

    # Risk Adjustment (never modifies raw_score)
    penalty, risk_rationale = calculate_risk_penalty(risks or [])
    risk_adjusted_score = round(max(0.0, raw_score - penalty), 1)

    rationale = {
        "customer_demand": f"Score {demand_score:.1f}: Based on {len(evidence_ids)} verified citations with evidence factor {ev_factor:.2f}.",
        "competitive_gap": f"Score {gap_score:.1f}: Evaluated against {len(opportunity.get('relevant_competitors', []))} direct/indirect market players.",
        "commercial_attractiveness": f"Score {comm_score:.1f}: Business model: '{opportunity.get('commercial_model', 'standard')[:60]}...'.",
        "implementation_feasibility": f"Score {feas_score:.1f}: Factored {len(barriers)} operational friction barriers.",
        "market_growth": f"Score {growth_score:.1f}: Sector growth baseline.",
        "strategic_differentiation": f"Score {diff_score:.1f}: Value prop clarity: '{opportunity.get('competitive_differentiation', '')[:60]}...'.",
        "risk_adjustment": risk_rationale,
    }

    return OpportunityScore(
        opportunity_id=opp_id,
        raw_score=raw_score,
        risk_adjusted_score=risk_adjusted_score,
        component_scores=components,
        dimension_weights=weights,
        scoring_rationale=rationale,
        evidence_ids=evidence_ids,
        missing_information=opportunity.get("additional_research_required", []),
        uncertainty="low" if ev_factor > 0.8 else "moderate",
        scoring_version="2.0-deterministic",
    )
