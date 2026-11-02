"""
Opportunity Scoring Service Package for MARKETPULSE Stage 2.
"""

from app.services.opportunity_scoring.dimensions import DEFAULT_DIMENSION_WEIGHTS, validate_weights
from app.services.opportunity_scoring.evidence_assessment import assess_evidence_quality_factor
from app.services.opportunity_scoring.risk_adjustment import calculate_risk_penalty
from app.services.opportunity_scoring.scorer import score_opportunity
from app.services.opportunity_scoring.ranking import rank_opportunities

__all__ = [
    "DEFAULT_DIMENSION_WEIGHTS",
    "validate_weights",
    "assess_evidence_quality_factor",
    "calculate_risk_penalty",
    "score_opportunity",
    "rank_opportunities",
]
