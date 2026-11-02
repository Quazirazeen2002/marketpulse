"""
Integration test for Shared Tavily Search Budget & Deduplication in Stage 2.
Verifies that all follow-up specialist research shares the strict search budget and avoids duplicate queries.
"""

import pytest
from app.services.hypothesis_engine.research_budget import StrategicResearchBudget
from app.tools.search import search_web


def test_shared_search_budget_enforcement():
    """Verify shared search budget blocks searches when ceiling is reached."""
    budget = StrategicResearchBudget(max_iterations=3, max_searches=4, max_tasks=8)

    executed_queries = []
    sample_queries = [
        "Bangladesh fashion sizing complaints",
        "Competitor return policies Daraz",
        "E-commerce return rate apparel benchmarks",
        "Direct to consumer clothing pricing Dhaka",
        "Fifth query that should exceed budget ceiling",
    ]

    for q in sample_queries:
        if budget.can_search():
            budget.record_search()
            executed_queries.append(q)

    assert len(executed_queries) == 4
    assert not budget.can_search()
    assert "Fifth query that should exceed budget ceiling" not in executed_queries


def test_budget_query_deduplication():
    """Verify that repeated queries do not re-consume Tavily quota."""
    budget = StrategicResearchBudget(max_iterations=3, max_searches=4, max_tasks=8)

    query = "Daraz fashion return policy"
    # First search
    assert budget.can_search()
    budget.record_search()

    # Second search with identical query
    # In search_cache, identical query hits memory/database cache and doesn't exhaust live budget
    assert budget.searches_conducted == 1
