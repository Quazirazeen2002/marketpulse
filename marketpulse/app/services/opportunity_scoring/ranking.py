"""
Opportunity Ranking and Prioritization Engine.
"""

from typing import List, Dict, Any, Tuple
from app.schemas.strategic import OpportunityScore


def rank_opportunities(
    opportunities: List[Dict[str, Any]],
    scores: Dict[str, OpportunityScore],
) -> List[Dict[str, Any]]:
    """
    Rank opportunity records based on risk_adjusted_score (descending),
    preserving both raw and risk-adjusted scores.
    """
    ranked = []
    for opp in opportunities:
        opp_id = opp.get("opportunity_id", "")
        score_obj = scores.get(opp_id)
        if score_obj:
            entry = {
                **opp,
                "raw_score": score_obj.raw_score,
                "risk_adjusted_score": score_obj.risk_adjusted_score,
                "component_scores": score_obj.component_scores,
                "scoring_rationale": score_obj.scoring_rationale,
            }
        else:
            entry = {
                **opp,
                "raw_score": 0.0,
                "risk_adjusted_score": 0.0,
                "component_scores": {},
                "scoring_rationale": {},
            }
        ranked.append(entry)

    ranked.sort(key=lambda x: x.get("risk_adjusted_score", 0.0), reverse=True)
    return ranked
