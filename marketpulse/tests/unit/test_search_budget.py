"""
Unit tests for ResearchSearchBudget.
Verifies run-level budget enforcement, shared concurrency ceilings across parallel agents,
and SearchBudgetExceededError generation.
"""

from concurrent.futures import ThreadPoolExecutor
import pytest
from app.services.web_search.search import ResearchSearchBudget
from app.services.web_search.exceptions import SearchBudgetExceededError


def test_budget_enforcement_basic():
    budget = ResearchSearchBudget(max_searches_per_run=3)
    run_id = "test-run-1"

    assert budget.can_search(run_id)
    budget.record_search(run_id, query="Query 1")
    assert budget.get_count(run_id) == 1

    budget.record_search(run_id, query="Query 2")
    budget.record_search(run_id, query="Query 3")
    assert budget.get_count(run_id) == 3
    assert not budget.can_search(run_id)

    # 4th search must raise SearchBudgetExceededError
    with pytest.raises(SearchBudgetExceededError) as exc_info:
        budget.record_search(run_id, query="Query 4")

    assert exc_info.value.max_budget == 3
    assert exc_info.value.current_count == 3


def test_parallel_agent_shared_budget():
    """Simulate 3 parallel specialist agents competing for a shared run budget of 6 queries."""
    budget = ResearchSearchBudget(max_searches_per_run=6)
    run_id = "shared-parallel-run"

    def agent_search_task(agent_name: str, query_num: int):
        query = f"[{agent_name}] Research query {query_num}"
        try:
            budget.record_search(run_id, query=query)
            return True
        except SearchBudgetExceededError:
            return False

    tasks = [
        ("Market Analyst", 1), ("Market Analyst", 2), ("Market Analyst", 3),
        ("Competitor Analyst", 1), ("Competitor Analyst", 2), ("Competitor Analyst", 3),
        ("Customer Analyst", 1), ("Customer Analyst", 2), ("Customer Analyst", 3),
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda t: agent_search_task(*t), tasks))

    # Exactly 6 should succeed and 3 should fail due to shared ceiling
    successful = sum(1 for r in results if r is True)
    exceeded = sum(1 for r in results if r is False)

    assert successful == 6
    assert exceeded == 3
    assert budget.get_count(run_id) == 6

    stats = budget.get_run_stats(run_id)
    assert stats["searches_executed"] == 6
    assert stats["remaining_budget"] == 0
    assert len(stats["query_history"]) == 6
