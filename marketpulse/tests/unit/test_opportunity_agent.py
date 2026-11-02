"""
Unit tests for Opportunity Discovery Analyst.
Validates autonomous opportunity discovery, hypothesis linking, and structured OpportunityRecord generation.
"""

import pytest
from app.agents.opportunity_analyst import run_opportunity_analyst, AGENT_NAME
from app.models.gateway import get_model_for_agent
from app.schemas.strategic import OpportunityRecord


def test_opportunity_analyst_model_assignment():
    """Verify Opportunity Analyst uses spark-1.3 exclusively."""
    assert AGENT_NAME == "Opportunity Discovery Analyst"
    model = get_model_for_agent(AGENT_NAME)
    assert model.model_name == "spark-1.3"


def test_opportunity_discovery_execution():
    """Test autonomous generation of structured opportunity records."""
    res = run_opportunity_analyst(
        objective="Investigate fashion e-commerce in Bangladesh",
        industry="Fashion E-Commerce",
        geography="Bangladesh",
        market_findings={"market_structure": "Growing fast"},
        competitor_findings={"direct_competitors": ["Daraz", "Aarong"]},
        customer_findings={"unmet_needs": ["Fit guidance", "Reliable delivery"]},
        evidence_records=[{"evidence_id": "ev-daraz-1"}, {"evidence_id": "ev-review-2"}],
    )

    assert res["agent_name"] == "Opportunity Discovery Analyst"
    assert "opportunity_report" in res
    assert res["opportunity_report"]["model_name"] == "spark-1.3"
    assert "opportunities" in res
    assert len(res["opportunities"]) >= 2

    opp0 = res["opportunities"][0]
    assert opp0["opportunity_id"].startswith("OPP-")
    assert opp0["problem_statement"] != ""
    assert "ev-daraz-1" in opp0["supporting_evidence_ids"]
    assert opp0["target_customer"] != ""
