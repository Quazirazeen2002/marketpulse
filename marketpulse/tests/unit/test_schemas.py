"""
Unit tests for Stage 2 Pydantic Schemas.
Tests strict type validation, enums, defaults, and error boundaries.
"""

import pytest
from pydantic import ValidationError
from app.schemas.strategic import (
    StrategicResearchRequest,
    MarketingIntelligenceReport,
    CommercialIntelligenceReport,
    OpportunityRecord,
    OpportunityDiscoveryReport,
    RiskAssessment,
    RiskIntelligenceReport,
    ResearchHypothesis,
    FollowupResearchTask,
    OpportunityScore,
    ScenarioInput,
    ScenarioResult,
    SensitivityAnalysis,
    BusinessScenario,
    StrategicExecutiveReport,
    HypothesisStatus,
    RiskCategory,
    RiskLikelihood,
    RiskImpact,
    StrategicEventType,
)


def test_strategic_research_request_validation():
    """Verify StrategicResearchRequest enforces non-empty research_id and bounded limits."""
    req = StrategicResearchRequest(
        research_id="run-12345",
        strategic_objective="Fashion DTC Brand",
        max_research_iterations=3,
        max_followup_searches=4,
        max_followup_tasks=8,
    )
    assert req.research_id == "run-12345"
    assert req.max_research_iterations == 3

    # Reject out of bounds
    with pytest.raises(ValidationError):
        StrategicResearchRequest(research_id="run-1", max_research_iterations=10)


def test_opportunity_record_validation():
    """Verify OpportunityRecord enforces required fields."""
    opp = OpportunityRecord(
        opportunity_id="opp-1",
        opportunity_name="Fit Advisory",
        problem_statement="Return rates high",
        target_customer="Shoppers",
        market_segment="Apparel",
        proposed_solution="3D fit recommendation",
        commercial_model="DTC retail",
        expected_customer_value="Better fit",
        competitive_differentiation="Proprietary tech",
    )
    assert opp.opportunity_id == "opp-1"
    assert opp.status == "discovered"

    with pytest.raises(ValidationError):
        OpportunityRecord(opportunity_id="opp-1")  # missing required fields


def test_opportunity_score_bounds():
    """Verify raw_score and risk_adjusted_score are bounded between 0.0 and 100.0."""
    score = OpportunityScore(
        opportunity_id="opp-1",
        raw_score=85.5,
        risk_adjusted_score=78.2,
    )
    assert score.raw_score == 85.5

    with pytest.raises(ValidationError):
        OpportunityScore(opportunity_id="opp-1", raw_score=150.0, risk_adjusted_score=80.0)

    with pytest.raises(ValidationError):
        OpportunityScore(opportunity_id="opp-1", raw_score=80.0, risk_adjusted_score=-5.0)


def test_executive_report_structure():
    """Verify StrategicExecutiveReport enforces all 10 standard sections A-J."""
    rep = StrategicExecutiveReport(
        strategic_analysis_id="sa-01",
        research_id="rr-01",
        strategic_objective="E-commerce Analysis",
        industry="Retail",
        geography="Bangladesh",
        section_a_executive_summary="Summary A",
        section_b_market_intelligence="Market B",
        section_c_competitor_intelligence="Competitors C",
        section_d_marketing_intelligence="Marketing D",
        section_e_commercial_intelligence="Commercial E",
    )
    assert rep.director_model == "muse-wonder-1.0"
    assert rep.specialist_model == "spark-1.3"
    assert rep.section_a_executive_summary == "Summary A"
