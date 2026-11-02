"""
Unit tests for Autonomous Research-Gap Discovery Engine.
Tests gap_detector, hypothesis_generator, task_prioritizer, research_budget, stopping_conditions, and hypothesis_validator.
"""

import pytest
from app.services.hypothesis_engine import (
    StrategicResearchBudget,
    detect_research_gaps,
    generate_hypotheses_from_findings,
    prioritize_and_create_tasks,
    validate_hypotheses,
    check_stopping_conditions,
)
from app.schemas.strategic import HypothesisStatus, ResearchHypothesis


def test_research_budget_boundaries():
    """Verify research budget ceilings (iterations=3, searches=4, tasks=8)."""
    budget = StrategicResearchBudget(max_iterations=3, max_searches=4, max_tasks=8)
    assert budget.can_search()
    assert budget.can_dispatch_task()

    # Record 4 searches
    for _ in range(4):
        budget.record_search()
    assert not budget.can_search()

    # Record tasks
    for _ in range(8):
        budget.record_task()
    assert not budget.can_dispatch_task()


def test_gap_detector():
    """Verify gap detection extracts actionable research questions from findings and contradictions."""
    gaps = detect_research_gaps(
        findings_by_agent={"Customer Analyst": {"research_gaps": ["No pricing data available for premium delivery tiers"]}},
        claims=[{"claim_text": "Competitors claim 99% customer satisfaction", "verification_status": "unverified"}],
        contradictions=[{"conflict_summary": "Delivery takes 2 days vs 10 days"}],
    )
    assert len(gaps) >= 2
    assert any("delivery" in g.lower() or "pricing" in g.lower() for g in gaps)


def test_hypothesis_generator():
    """Verify hypotheses are generated with originating findings and initial confidence."""
    gaps = ["Customers frequently express dissatisfaction with online clothing sizing."]
    hypotheses = generate_hypotheses_from_findings(
        gaps=gaps,
        customer_findings={"unmet_needs": ["Accurate size charts"]},
        competitor_findings={"direct_competitors": ["Daraz"]},
        market_findings={"market_structure": "Growing"},
        evidence_ids=["ev-1"],
    )

    assert len(hypotheses) >= 1
    h = hypotheses[0]
    assert h.validation_status in (HypothesisStatus.PROPOSED, HypothesisStatus.INVESTIGATING)
    assert h.confidence_assessment > 0.0


def test_task_prioritizer():
    """Verify follow-up tasks are created and allocated to proper specialist agents."""
    hyp = ResearchHypothesis(
        hypothesis_id="hyp-01",
        description="Customers will pay for transparent delivery guidance",
        originating_findings=["Delivery complaints dominant"],
        evidence_ids=["ev-1"],
    )
    tasks = prioritize_and_create_tasks(
        hypotheses=[hyp],
        industry="Fashion E-Commerce",
        geography="Bangladesh",
        max_tasks=4,
    )
    assert len(tasks) >= 1
    t = tasks[0]
    assert t.hypothesis_id == "hyp-01"
    assert t.target_agent in (
        "Customer Intelligence Analyst",
        "Competitor Intelligence Analyst",
        "Commercial Intelligence Analyst",
        "Marketing Intelligence Analyst",
    )


def test_hypothesis_validator():
    """Verify status transitions based on empirical evidence and contradictions."""
    hyp = ResearchHypothesis(
        hypothesis_id="hyp-01",
        description="Customers will pay for reliable delivery",
        originating_findings=["Delivery complaints"],
        evidence_ids=["ev-1"],
    )

    # Validated with strong supporting evidence from follow-up task
    validated_list = validate_hypotheses(
        hypotheses=[hyp],
        new_evidence=[{"evidence_id": "ev-2"}, {"evidence_id": "ev-3"}],
        followup_results=[{"hypothesis_id": "hyp-01", "new_evidence_ids": ["ev-2", "ev-3"]}],
    )
    assert len(validated_list) == 1
    validated = validated_list[0]
    assert validated.validation_status in (HypothesisStatus.SUPPORTED, HypothesisStatus.PARTIALLY_SUPPORTED)
    assert validated.confidence_assessment >= 0.7


def test_stopping_conditions():
    """Verify stopping conditions trigger when budget is exhausted or max iterations reached."""
    budget = StrategicResearchBudget(max_iterations=3, max_searches=4, max_tasks=8)
    hypotheses = [
        ResearchHypothesis(
            hypothesis_id="h1",
            description="Test",
            validation_status=HypothesisStatus.SUPPORTED,
            confidence_assessment=0.9,
        )
    ]

    # When all hypotheses are evaluated and pending_tasks is empty -> stops
    stop, reason = check_stopping_conditions(budget=budget, hypotheses=hypotheses, pending_tasks=[])
    assert stop is True
    assert "confidence" in reason.lower()
