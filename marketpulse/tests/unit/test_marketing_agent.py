"""
Unit tests for Marketing Intelligence Analyst.
Validates brand positioning, campaign intelligence, channel intelligence, and marketing gap detection.
Verifies spark-1.3 model assignment and non-fabrication of private ad metrics.
"""

import pytest
from unittest.mock import patch
from app.agents.marketing_analyst import run_marketing_analyst, AGENT_NAME
from app.models.gateway import get_model_for_agent
from app.schemas.strategic import MarketingIntelligenceReport


def test_marketing_analyst_model_assignment():
    """Verify Marketing Analyst uses spark-1.3 exclusively."""
    assert AGENT_NAME == "Marketing Intelligence Analyst"
    model = get_model_for_agent(AGENT_NAME)
    assert model.model_name == "spark-1.3"


def test_marketing_analyst_execution():
    """Test marketing analysis output structure and gap detection."""
    mock_specialist_result = {
        "agent_name": AGENT_NAME,
        "summary": "Competitors compete heavily on price flash sales but overlook fit and delivery trust.",
        "evidence_ids": ["ev-marketing-1", "ev-marketing-2"],
        "key_findings": ["Discounts dominate", "Trust is weak"],
    }

    with patch("app.agents.marketing_analyst.run_specialist", return_value=mock_specialist_result):
        res = run_marketing_analyst(
            objective="Analyze fashion e-commerce marketing in Bangladesh",
            queries=["fashion marketing Bangladesh"],
            industry="Fashion E-Commerce",
            geography="Bangladesh",
        )

    assert "marketing_report" in res
    m_rep = res["marketing_report"]
    assert m_rep["agent_name"] == "Marketing Intelligence Analyst"
    assert m_rep["model_name"] == "spark-1.3"
    assert len(m_rep["marketing_gaps"]) >= 1
    assert "Private advertising expenditure (ad spend) is not publicly disclosed" in m_rep["unknown_metrics"]
    assert "positioning_themes" in m_rep["brand_intelligence"]
    assert "ev-marketing-1" in m_rep["supporting_evidence_ids"]
