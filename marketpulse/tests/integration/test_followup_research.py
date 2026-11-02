"""
Integration test for Autonomous Follow-up Research Loops.
Verifies that hypotheses trigger follow-up research tasks, collect evidence, update validation status,
and stop when iteration or budget ceiling is reached.
"""

import pytest
from app.services.hypothesis_engine import (
    StrategicResearchBudget,
    detect_research_gaps,
    generate_hypotheses_from_gaps,
    prioritize_followup_tasks,
    validate_hypothesis,
    should_stop_research_loop,
)
from app.graph.strategic_routing import should_execute_followup
from app.schemas.strategic import HypothesisStatus, ResearchHypothesis


def test_autonomous_followup_routing_condition():
    """Verify routing directs to followup_investigation when hypotheses are under-investigated."""
    state_with_investigating_hypotheses = {
        "hypotheses": [
            ResearchHypothesis(
                hypothesis_id="h1",
                description="Customers will pay for sizing guidance",
                validation_status=HypothesisStatus.INVESTIGATING,
                confidence_score=0.4,
            )
        ],
        "research_iterations": 1,
        "search_budget": {"max_iterations": 3, "max_searches": 4, "max_tasks": 8},
    }

    next_node = should_execute_followup(state_with_investigating_hypotheses)
    assert next_node == "followup_investigation"


def test_autonomous_routing_stops_at_max_iterations():
    """Verify routing diverts to opportunity_scoring when max iterations reached."""
    state_at_ceiling = {
        "hypotheses": [
            ResearchHypothesis(
                hypothesis_id="h1",
                description="Under-investigated hypothesis",
                validation_status=HypothesisStatus.INVESTIGATING,
                confidence_score=0.4,
            )
        ],
        "research_iterations": 3,  # Reached ceiling of 3
        "search_budget": {"max_iterations": 3, "max_searches": 4, "max_tasks": 8},
    }

    next_node = should_execute_followup(state_at_ceiling)
    assert next_node == "opportunity_scoring"


def test_hypothesis_status_lifecycle():
    """Verify complete hypothesis lifecycle from proposed -> investigating -> supported."""
    budget = StrategicResearchBudget(max_iterations=3, max_searches=4, max_tasks=8)

    # 1. Gaps detected
    gaps = detect_research_gaps(
        contradictions=[],
        unverified_claims=["Competitors state 98% satisfaction on fit"],
        specialist_gaps=["Fit accuracy data missing"],
    )
    assert len(gaps) > 0

    # 2. Hypothesis generated
    hyps = generate_hypotheses_from_gaps(gaps, strategic_objective="Fashion fit")
    h0 = hyps[0]
    assert h0.validation_status == HypothesisStatus.PROPOSED

    # 3. Tasks prioritized
    tasks = prioritize_followup_tasks(hyps, max_tasks=4)
    assert len(tasks) > 0
    budget.record_task()

    # 4. Investigation executes & collects evidence
    h0.validation_status = HypothesisStatus.INVESTIGATING
    validated = validate_hypothesis(
        h0,
        new_evidence=["ev-survey-1", "ev-market-2"],
        contradictions=[],
    )

    # 5. Transitioned to supported
    assert validated.validation_status in (HypothesisStatus.SUPPORTED, HypothesisStatus.PARTIALLY_SUPPORTED)
    assert validated.confidence_score >= 0.7
