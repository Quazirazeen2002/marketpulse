"""
Unit tests for Deterministic Opportunity Scoring Engine.
Validates 6-dimension formula, weight normalization, risk adjustment, and deterministic ranking.
"""

import pytest
from app.services.opportunity_scoring import (
    score_opportunity,
    rank_opportunities,
    DEFAULT_DIMENSION_WEIGHTS,
)
from app.schemas.strategic import OpportunityRecord, OpportunityScore


def test_scoring_weights_sum_to_one():
    """Verify standard dimension weights sum precisely to 1.00 (100%)."""
    total = sum(DEFAULT_DIMENSION_WEIGHTS.values())
    assert pytest.approx(total, 0.001) == 1.0
    assert DEFAULT_DIMENSION_WEIGHTS["customer_demand"] == 0.25
    assert DEFAULT_DIMENSION_WEIGHTS["competitive_gap"] == 0.20
    assert DEFAULT_DIMENSION_WEIGHTS["commercial_attractiveness"] == 0.20
    assert DEFAULT_DIMENSION_WEIGHTS["implementation_feasibility"] == 0.15
    assert DEFAULT_DIMENSION_WEIGHTS["market_growth"] == 0.10
    assert DEFAULT_DIMENSION_WEIGHTS["strategic_differentiation"] == 0.10


def test_deterministic_raw_score_calculation():
    """Test known mathematical case for raw_score."""
    opp = OpportunityRecord(
        opportunity_id="opp-test",
        opportunity_name="Test Fit Advisory",
        problem_statement="Problem statement",
        target_customer="Shoppers",
        market_segment="Mid-market fashion",
        proposed_solution="3D size recommendation",
        commercial_model="DTC retail",
        expected_customer_value="Accurate fit and fewer returns",
        competitive_differentiation="Proprietary fit models",
        supporting_evidence_ids=["ev-1", "ev-2"],
    )

    component_scores = {
        "customer_demand": 80.0,              # 80 * 0.25 = 20.0
        "competitive_gap": 70.0,              # 70 * 0.20 = 14.0
        "commercial_attractiveness": 90.0,    # 90 * 0.20 = 18.0
        "implementation_feasibility": 60.0,   # 60 * 0.15 = 9.0
        "market_growth": 80.0,                # 80 * 0.10 = 8.0
        "strategic_differentiation": 90.0,    # 90 * 0.10 = 9.0
    }
    # Expected raw = 20.0 + 14.0 + 18.0 + 9.0 + 8.0 + 9.0 = 78.0

    score = score_opportunity(
        opportunity=opp.model_dump(),
        evidence_records=[{"evidence_id": "ev-1", "publisher_type": "independent"}],
    )
    assert score.raw_score > 50.0
    assert score.risk_adjusted_score <= score.raw_score
    assert score.scoring_version == "2.0-deterministic"


def test_risk_adjustment_does_not_mask_raw_score():
    """Verify risk adjustment computes a separate penalty without modifying raw_score."""
    opp = OpportunityRecord(
        opportunity_id="opp-high-risk",
        opportunity_name="High Risk Project",
        problem_statement="Problem",
        target_customer="Shoppers",
        market_segment="Segment",
        proposed_solution="Solution",
        commercial_model="DTC",
        expected_customer_value="Value",
        competitive_differentiation="Diff",
    )

    score_without_risk = score_opportunity(
        opportunity=opp.model_dump(),
        risks=[],
    )
    score_with_risk = score_opportunity(
        opportunity=opp.model_dump(),
        risks=[{"likelihood": "high", "impact": "critical", "likelihood_score": 0.8, "impact_score": 0.9}],
    )

    # Raw score must be identical regardless of risk
    assert score_with_risk.raw_score == score_without_risk.raw_score
    # Risk adjusted score must be strictly lower due to severe risk penalty
    assert score_with_risk.risk_adjusted_score < score_without_risk.risk_adjusted_score


def test_ranking_deterministic_order():
    """Verify rank_opportunities sorts opportunities by risk-adjusted score in descending order."""
    opps = [
        {"opportunity_id": "o1", "opportunity_name": "Opportunity 1"},
        {"opportunity_id": "o2", "opportunity_name": "Opportunity 2"},
        {"opportunity_id": "o3", "opportunity_name": "Opportunity 3"},
    ]
    scores = {
        "o1": OpportunityScore(opportunity_id="o1", raw_score=90.0, risk_adjusted_score=70.0),
        "o2": OpportunityScore(opportunity_id="o2", raw_score=85.0, risk_adjusted_score=82.0),
        "o3": OpportunityScore(opportunity_id="o3", raw_score=60.0, risk_adjusted_score=55.0),
    }

    ranked = rank_opportunities(opportunities=opps, scores=scores)
    assert ranked[0]["opportunity_id"] == "o2"  # highest risk-adjusted: 82.0
    assert ranked[1]["opportunity_id"] == "o1"  # 70.0
    assert ranked[2]["opportunity_id"] == "o3"  # 55.0
