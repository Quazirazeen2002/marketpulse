"""
Integration test for full MARKETPULSE research workflow using Tavily search service.
Executes LangGraph StateGraph with mocked Tavily results, verifying that:
1. Research Director plans queries.
2. Market, Competitor, and Customer analysts query Tavily and acquire evidence.
3. Provenance and search_provider are correctly set to 'tavily'.
4. Claims are extracted, verified, and executive report is synthesized.
"""

from unittest.mock import patch
import uuid
import pytest

from app.graph.builder import marketpulse_graph
from app.services.web_search.search import budget_manager


def test_full_langgraph_workflow_with_tavily():
    run_id = f"test-workflow-{uuid.uuid4().hex[:8]}"
    budget_manager.reset_run(run_id)

    mock_tavily_results = [
        {
            "evidence_id": "mockev1001",
            "title": "South Asia Quick Commerce Market Review 2026",
            "url": "https://industry-insights.com/south-asia-qcommerce",
            "content": "Quick commerce in Dhaka reached $1.2B in 2025 with 35% year-on-year growth.",
            "publisher": "industry-insights.com",
            "score": 0.95,
            "query": "quick commerce trends",
            "search_provider": "tavily",
            "source_type": "tavily_search",
            "published_date": "2026-01-20",
        },
        {
            "evidence_id": "mockev1002",
            "title": "Grocery Logistics and Competitive Delivery Dynamics",
            "url": "https://logistics-daily.org/bangladesh-grocery",
            "content": "Major players maintain 15 to 30 minute delivery SLAs using micro-fulfillment centers.",
            "publisher": "logistics-daily.org",
            "score": 0.91,
            "query": "grocery delivery competitors",
            "search_provider": "tavily",
            "source_type": "tavily_search",
            "published_date": "2026-02-05",
        },
    ]

    initial_state = {
        "research_id": run_id,
        "research_objective": "Analyze quick commerce growth, competitor positioning, and customer delivery pain points in Bangladesh.",
        "industry": "E-commerce & Logistics",
        "geography": "Bangladesh",
        "time_horizon": "Current (Real-time)",
        "research_status": "pending",
        "iteration_count": 0,
        "evidence_registry": [],
        "errors": [],
    }

    # Patch search_web, get_director_model, and get_specialist_model for fast, deterministic testing
    with patch("app.agents.specialist.search_web", return_value=mock_tavily_results), \
         patch("app.agents.research_director.get_director_model", return_value=None), \
         patch("app.agents.specialist.get_specialist_model", return_value=None):
        final_state = marketpulse_graph.invoke(initial_state, config={"recursion_limit": 25})


    assert final_state["research_id"] == run_id
    assert final_state["research_status"] == "completed"



    # Verify that plan was formed
    plan = final_state.get("research_plan", {})
    assert len(plan.get("research_questions", [])) > 0

    # Verify specialist reports exist
    assert "market_report" in final_state
    assert "competitor_report" in final_state
    assert "customer_report" in final_state

    # Verify evidence provenance
    evidence = final_state.get("evidence_registry", [])
    assert len(evidence) > 0
    for ev in evidence:
        ev_dict = ev if isinstance(ev, dict) else ev.model_dump()
        assert ev_dict["search_provider"] == "tavily"
        assert ev_dict["evidence_id"]

    # Verify final executive report
    report = final_state.get("final_report", {})
    assert report.get("executive_summary")
    assert "status_dimensions" in final_state
