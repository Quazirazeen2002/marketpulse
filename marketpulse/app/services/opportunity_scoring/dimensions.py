"""
Opportunity Scoring Dimensions and Configurable Weights for MARKETPULSE Stage 2.
"""

from typing import Dict


DEFAULT_DIMENSION_WEIGHTS: Dict[str, float] = {
    "customer_demand": 0.25,
    "competitive_gap": 0.20,
    "commercial_attractiveness": 0.20,
    "implementation_feasibility": 0.15,
    "market_growth": 0.10,
    "strategic_differentiation": 0.10,
}


def validate_weights(weights: Dict[str, float]) -> bool:
    """Ensure weights sum to 1.0 within tolerance."""
    total = sum(weights.values())
    return abs(total - 1.0) < 1e-4
