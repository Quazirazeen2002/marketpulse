"""
Risk-Adjustment Calculator for Opportunity Scoring.
Computes a separate, transparent risk-adjusted assessment alongside the raw score.
Never modifies or conceals the raw opportunity score.
"""

from typing import List, Dict, Any, Tuple


def calculate_risk_penalty(risks: List[Dict[str, Any]]) -> Tuple[float, str]:
    """
    Calculate risk deduction multiplier (0.0 to 35.0 points deduction)
    based on likelihood and impact of opportunity-associated risks.
    """
    if not risks:
        return 5.0, "Low risk profile: minimal recorded operational vulnerabilities."

    total_risk_exposure = 0.0
    critical_count = 0

    for r in risks:
        lh = float(r.get("likelihood_score", 0.5))
        imp = float(r.get("impact_score", 0.5))
        risk_val = lh * imp
        total_risk_exposure += risk_val

        if r.get("likelihood") == "high" and r.get("impact") in ("high", "critical"):
            critical_count += 1

    # Base penalty from accumulated risk exposure
    penalty = min(total_risk_exposure * 12.0, 25.0)

    # Extra penalty for critical concurrent risks
    if critical_count > 0:
        penalty = min(penalty + (critical_count * 5.0), 35.0)

    rationale = (
        f"Assessed {len(risks)} risk factors ({critical_count} severe). "
        f"Applied risk discount factor of {penalty:.1f} points based on operational, "
        "adoption, and competitive retaliation probabilities."
    )
    return penalty, rationale


def compute_risk_penalty(risks: List[Dict[str, Any]]) -> float:
    """Helper returning just the numeric risk penalty."""
    penalty, _ = calculate_risk_penalty(risks)
    return penalty
