"""
Unit tests for Risk Assessment Services.
Validates transparent qualitative/quantitative risk metrics, categories, likelihood and impact scales.
"""

import pytest
from app.schemas.strategic import (
    RiskCategory,
    RiskLikelihood,
    RiskImpact,
    RiskAssessment,
)
from app.services.opportunity_scoring.risk_adjustment import compute_risk_penalty


def test_risk_categories_enumeration():
    """Verify all 9 standard risk categories are covered."""
    categories = {c.value for c in RiskCategory}
    assert "operational" in categories
    assert "financial" in categories
    assert "customer_adoption" in categories
    assert "competitive_retaliation" in categories
    assert "market_saturation" in categories
    assert "regulatory" in categories
    assert "economic" in categories
    assert "technology" in categories
    assert "supply_chain" in categories


def test_risk_penalty_computation():
    """Verify compute_risk_penalty calculates proportional transparent penalties."""
    # Zero risks -> baseline 5.0 minimal buffer
    assert compute_risk_penalty([]) == 5.0

    # Low risk -> small penalty
    low_penalty = compute_risk_penalty([{"likelihood": "low", "impact": "low", "likelihood_score": 0.3, "impact_score": 0.3}])
    assert low_penalty <= 15.0

    # Critical risk -> larger penalty
    crit_penalty = compute_risk_penalty([{"likelihood": "critical", "impact": "critical"}])
    assert crit_penalty > low_penalty
    assert crit_penalty <= 40.0  # Max ceiling cap


def test_risk_assessment_validation():
    """Verify RiskAssessment model validates required mitigation and evidence references."""
    assessment = RiskAssessment(
        risk_id="RSK-10",
        opportunity_id="opp-1",
        risk_category=RiskCategory.SUPPLY_CHAIN,
        risk_description="Port congestion delays garment import fabric",
        likelihood=RiskLikelihood.HIGH,
        impact=RiskImpact.MEDIUM,
        mitigation_strategy="Diversify local fabric mills",
        residual_risk="medium",
        evidence_ids=["ev-port-1"],
    )

    assert assessment.risk_id == "RSK-10"
    assert assessment.likelihood == "high"
    assert "ev-port-1" in assessment.evidence_ids
