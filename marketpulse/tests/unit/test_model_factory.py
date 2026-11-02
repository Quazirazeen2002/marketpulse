"""
Unit tests for Centralized Model Factory and Model Allocation Constraints.
Verifies Research Director uses Muse Wonder exclusively and all 7 specialists use Spark 1.3 exclusively.
"""

import pytest
from app.models.gateway import (
    get_director_model,
    get_specialist_model,
    get_model_for_agent,
    SPECIALIST_ROLES,
)


def test_research_director_model_allocation():
    """Verify Research Director is strictly allocated Meta Muse Wonder (muse-wonder-1.0)."""
    director_model = get_director_model()
    assert director_model.model_name == "muse-wonder-1.0"

    # Via unified factory
    factory_director = get_model_for_agent("Research Director")
    assert factory_director.model_name == "muse-wonder-1.0"


def test_all_seven_specialists_model_allocation():
    """Verify all 7 specialist agents are strictly allocated Meta Spark 1.3 (spark-1.3)."""

    expected_specialists = [
        "Market Intelligence Analyst",
        "Competitor Intelligence Analyst",
        "Customer Intelligence Analyst",
        "Marketing Intelligence Analyst",
        "Commercial Intelligence Analyst",
        "Opportunity Discovery Analyst",
        "Risk & Industry Intelligence Analyst",
    ]

    for specialist_name in expected_specialists:
        assert specialist_name.lower() in SPECIALIST_ROLES
        model = get_model_for_agent(specialist_name)
        assert model.model_name == "spark-1.3", f"{specialist_name} must use spark-1.3 exclusively"


def test_no_silent_model_switching():
    """Confirm unknown or spoofed roles default strictly to spark-1.3 and never inherit Muse Wonder."""
    unknown_model = get_model_for_agent("Unauthorized Analyst")
    assert unknown_model.model_name == "spark-1.3"


def test_specialist_direct_model_helper():
    """Verify get_specialist_model returns spark-1.3."""
    spec_model = get_specialist_model()
    assert spec_model.model_name == "spark-1.3"
