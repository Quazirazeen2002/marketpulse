"""
Integration test for Strategic LangGraph StateGraph Execution.
Verifies full graph execution cycle from Stage 1 research load to final report persistence.
Uses deterministic mocked model responses.
"""

import pytest
from unittest.mock import MagicMock, patch
from app.graph.strategic_workflow import strategic_graph
from app.database.repository import save_complete_research_run, get_strategic_analysis


@pytest.fixture
def mock_stage1_research():
    """Seed a Stage 1 research run into SQLite."""
    run_state = {
        "research_id": "test-stage1-run-id",
        "research_objective": "Analyze the fashion e-commerce market in Bangladesh",
        "industry": "Fashion E-Commerce",
        "geography": "Bangladesh",
        "time_horizon": "Current",
        "market_report": {
            "market_structure": "Rapidly growing online market.",
            "cagr": "15-20%",
            "key_drivers": ["Smartphone penetration", "Young demographic"],
            "summary": "Market expanding quickly.",
        },
        "competitor_report": {
            "direct_competitors": ["Daraz", "Aarong"],
            "summary": "Competitors compete on discounts with poor sizing fit guidance.",
        },
        "customer_report": {
            "unmet_needs": ["Accurate size charts", "Transparent delivery tracking"],
            "complaints": ["High return rates due to bad fit"],
            "summary": "Customers want reliable fit advisory.",
        },
        "sources": [
            {
                "url": "https://example.com/source1",
                "title": "Fashion Market Report",
                "publisher": "Retail News",
                "full_text": "Fashion sales in Bangladesh growing 20% annually.",
                "quality_score": 0.85,
            }
        ],
        "evidence_registry": [
            {
                "evidence_id": "ev-stage1-001",
                "source_url": "https://example.com/source1",
                "supporting_excerpt": "Customer sizing issues generate 25% return rates.",
                "source_title": "Fashion Market Report",
                "publisher": "Retail News",
            }
        ],
        "claims": [],
        "verifications": [],
        "contradictions": [],
        "research_gaps": ["Delivery policy variances"],
    }
    save_complete_research_run(run_state)
    return "test-stage1-run-id"


def test_strategic_workflow_execution(mock_stage1_research):
    """Execute strategic workflow end-to-end and verify state transitions and output report."""
    initial_state = {
        "strategic_analysis_id": "test-strat-analysis-001",
        "research_id": mock_stage1_research,
        "strategic_objective": "Discover high-margin D2C opportunities with fit guidance",
        "research_iterations": 1,
        "search_budget": {"max_iterations": 1, "max_searches": 2, "max_tasks": 4},
        "execution_status": "running",
        "errors": [],
    }

    mock_specialist_output = {
        "agent_name": "Specialist Analyst",
        "summary": "Specialist analysis completed with verified findings.",
        "evidence_ids": ["ev-stage1-001"],
        "evidence": [{
            "evidence_id": "ev-stage1-001",
            "supporting_excerpt": "Customer sizing issues generate 25% return rates.",
            "source_url": "https://example.com/source1",
            "source_title": "Fashion Market Report",
            "publisher": "Retail News",
        }],
        "claims": [],
        "contradictions": [],
    }

    executed_nodes = []
    final_output = {}

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Executive synthesis and strategic plan.")

    with patch("app.agents.specialist.run_specialist", return_value=mock_specialist_output), \
         patch("app.agents.marketing_analyst.run_specialist", return_value=mock_specialist_output), \
         patch("app.agents.commercial_analyst.run_specialist", return_value=mock_specialist_output), \
         patch("app.graph.strategic_nodes.get_director_model", return_value=mock_llm), \
         patch("app.graph.strategic_nodes.get_specialist_model", return_value=mock_llm), \
         patch("app.agents.opportunity_analyst.get_specialist_model", return_value=mock_llm), \
         patch("app.agents.risk_analyst.get_specialist_model", return_value=mock_llm), \
         patch("app.models.gateway.get_specialist_model", return_value=mock_llm), \
         patch("app.models.gateway.get_director_model", return_value=mock_llm):
        for event in strategic_graph.stream(initial_state, config={"recursion_limit": 25}):
            for node_name, output in event.items():
                executed_nodes.append(node_name)
                final_output.update(output)

    assert "load_stage1_research" in executed_nodes
    assert "strategic_planning" in executed_nodes
    assert "parallel_specialists" in executed_nodes
    assert "strategic_synthesis" in executed_nodes
    assert "opportunity_scoring" in executed_nodes
    assert "strategic_executive_report" in executed_nodes
    assert "persist_strategic_analysis" in executed_nodes

    # Verify report was generated
    assert final_output.get("strategic_report") is not None
    rep = final_output["strategic_report"]
    dir_model = rep.get("director_model") if isinstance(rep, dict) else rep.director_model
    spec_model = rep.get("specialist_model") if isinstance(rep, dict) else rep.specialist_model
    exec_sum = rep.get("section_a_executive_summary") if isinstance(rep, dict) else rep.section_a_executive_summary
    assert dir_model == "muse-wonder-1.0"
    assert spec_model == "spark-1.3"
    assert exec_sum != ""

    # Verify persisted in database
    persisted = get_strategic_analysis("test-strat-analysis-001")
    assert persisted is not None
    assert persisted["status"] == "completed"
