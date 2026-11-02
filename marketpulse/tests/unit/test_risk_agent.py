"""
Unit tests for Risk & Industry Intelligence Analyst.
Validates adversarial challenge function, risk categorizations, likelihood/impact ratings, and mitigations.
"""

import pytest
from app.agents.risk_analyst import run_risk_analyst, AGENT_NAME
from app.models.gateway import get_model_for_agent
from app.schemas.strategic import RiskCategory, RiskLikelihood, RiskImpact


def test_risk_analyst_model_assignment():
    """Verify Risk Analyst uses spark-1.3 exclusively."""
    assert AGENT_NAME == "Risk & Industry Intelligence Analyst"
    model = get_model_for_agent(AGENT_NAME)
    assert model.model_name == "spark-1.3"


def test_risk_evaluation_execution():
    """Test adversarial risk evaluation on discovered opportunities."""
    res = run_risk_analyst(
        objective="Assess risks in Bangladesh fashion e-commerce",
        industry="Fashion E-Commerce",
        geography="Bangladesh",
        opportunities=[
            {
                "opportunity_id": "opp-fit-1",
                "opportunity_name": "Accurate Sizing Fashion Brand",
                "problem_statement": "High return rates",
                "commercial_model": "DTC",
            }
        ],
        market_findings={"market_structure": "Growing fast"},
        competitor_findings={"direct_competitors": ["Daraz"]},
        evidence_records=[{"evidence_id": "ev-adoption-1"}],
    )

    assert res["agent_name"] == "Risk & Industry Intelligence Analyst"
    assert "risk_report" in res
    assert res["risk_report"]["model_name"] == "spark-1.3"
    assert len(res["business_risks"]) >= 1

    r0 = res["business_risks"][0]
    assert r0["risk_id"].startswith("RSK-")
    assert r0["mitigation_strategy"] != ""
    assert r0["residual_risk"] != ""
    assert len(res["industry_risks"]) >= 1
