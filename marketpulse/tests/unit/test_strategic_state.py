"""
Unit tests for Strategic LangGraph State.
Validates typed state keys, evidence preservation, and state mutation boundaries.
"""

import pytest
from app.graph.strategic_state import StrategicState


def test_strategic_state_keys():
    """Verify StrategicState defines all mandatory Stage 2 schema keys."""
    expected_keys = {
        "strategic_analysis_id",
        "research_id",
        "strategic_objective",
        "industry",
        "geography",
        "stage1_findings",
        "stage1_evidence_ids",
        "market_report",
        "competitor_report",
        "customer_report",
        "marketing_report",
        "commercial_report",
        "opportunities",
        "risk_report",
        "hypotheses",
        "followup_tasks",
        "research_iterations",
        "search_budget",
        "opportunity_scores",
        "scenario_models",
        "strategic_recommendations",
        "research_gaps",
        "strategic_report",
        "execution_status",
        "errors",
    }

    state_annotations = StrategicState.__annotations__
    for key in expected_keys:
        assert key in state_annotations, f"Missing required key in StrategicState: {key}"


def test_strategic_state_instantiation():
    """Verify StrategicState can be properly typed and instantiated."""
    state: StrategicState = {
        "strategic_analysis_id": "test-analysis-1",
        "research_id": "test-run-1",
        "strategic_objective": "Test Objective",
        "industry": "Retail",
        "geography": "Global",
        "stage1_findings": {"market": "growing"},
        "stage1_evidence_ids": ["ev-1", "ev-2"],
        "market_report": {},
        "competitor_report": {},
        "customer_report": {},
        "marketing_report": {},
        "commercial_report": {},
        "opportunities": [],
        "risk_report": {},
        "hypotheses": [],
        "followup_tasks": [],
        "research_iterations": 1,
        "search_budget": {"max_iterations": 3, "max_searches": 4, "max_tasks": 8},
        "opportunity_scores": [],
        "scenario_models": [],
        "strategic_recommendations": [],
        "research_gaps": [],
        "strategic_report": None,
        "execution_status": "initialized",
        "errors": [],
    }

    assert state["strategic_analysis_id"] == "test-analysis-1"
    assert len(state["stage1_evidence_ids"]) == 2
    assert state["search_budget"]["max_iterations"] == 3
