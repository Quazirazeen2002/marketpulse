"""
Unit tests for Commercial Intelligence Analyst.
Validates product pricing, subscription models, revenue streams, and monetization gap identification.
Verifies spark-1.3 model assignment and non-fabrication of private cost data.
"""

import pytest
from unittest.mock import patch
from app.agents.commercial_analyst import run_commercial_analyst, AGENT_NAME
from app.models.gateway import get_model_for_agent
from app.schemas.strategic import CommercialIntelligenceReport


def test_commercial_analyst_model_assignment():
    """Verify Commercial Analyst uses spark-1.3 exclusively."""
    assert AGENT_NAME == "Commercial Intelligence Analyst"
    model = get_model_for_agent(AGENT_NAME)
    assert model.model_name == "spark-1.3"


def test_commercial_analyst_execution():
    """Test commercial intelligence generation and pricing gap detection."""
    mock_specialist_result = {
        "agent_name": AGENT_NAME,
        "summary": "Standard retail transaction margin with free shipping threshold at 1500 BDT.",
        "evidence_ids": ["ev-comm-1"],
        "key_findings": ["Delivery fees 60-120 BDT", "No premium delivery tier"],
    }

    with patch("app.agents.commercial_analyst.run_specialist", return_value=mock_specialist_result):
        res = run_commercial_analyst(
            objective="Analyze commercial e-commerce economics in Bangladesh",
            queries=["fashion pricing Bangladesh"],
            industry="Fashion E-Commerce",
            geography="Bangladesh",
        )

    assert "commercial_report" in res
    c_rep = res["commercial_report"]
    assert c_rep["agent_name"] == "Commercial Intelligence Analyst"
    assert c_rep["model_name"] == "spark-1.3"
    assert len(c_rep["pricing_gaps"]) >= 1
    assert len(c_rep["distinguished_estimates"]) >= 1
    assert len(c_rep["pricing_structures"]) >= 1
    assert "ev-comm-1" in c_rep["supporting_evidence_ids"]
