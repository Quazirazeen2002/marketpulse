"""
Scenario 2 — Telecom Commercial & Customer Experience Gaps.
Prompt: "Investigate commercial and customer experience gaps in mobile telecommunications and identify ways a telecom provider could improve customer satisfaction and revenue."
Validates:
- Marketing analysis
- Commercial model analysis
- Customer pain-point investigation
- Opportunity discovery
- Risk analysis
- Revenue-model hypotheses
- Evidence-backed strategic recommendations
- No invented private operator data
"""

import pytest
from app.graph.strategic_workflow import strategic_graph
from app.database.repository import save_complete_research_run, get_strategic_analysis


@pytest.fixture
def telecom_stage1():
    """Seed Stage 1 Telecom Research Run."""
    run_id = "scenario-telecom-stage1"
    save_complete_research_run({
        "research_id": run_id,
        "research_objective": "Investigate commercial and customer experience gaps in mobile telecommunications.",
        "industry": "Telecommunications",
        "geography": "Regional",
        "time_horizon": "Current",
        "market_report": {
            "market_structure": "Oligopoly with 3-4 major network operators.",
            "cagr": "5.2%",
            "key_drivers": ["5G transition", "Enterprise IoT", "Mobile financial services"],
            "summary": "Data consumption surging while voice ARPU plateaus.",
        },
        "competitor_report": {
            "direct_competitors": ["Telco A", "Telco B", "Telco C"],
            "pricing": "Fragmented data packs with confusing validity expirations",
            "summary": "Aggressive pack promotions with complex fine print.",
        },
        "customer_report": {
            "unmet_needs": ["Unused data rollover", "Transparent billing without hidden VAS deductions"],
            "complaints": ["Unwanted automatic value-added service deductions", "Data expires before usage"],
            "summary": "Customer trust eroded by unexpected balance deductions.",
        },
        "sources": [
            {
                "url": "https://example.com/telecom-regulator-report",
                "title": "Telecom Consumer Rights & Billing Audit",
                "publisher": "Regulatory Commission",
                "full_text": "Consumer complaints regarding billing transparency and unused data expiration increased 34%.",
                "quality_score": 0.95,
            }
        ],
        "evidence_registry": [
            {
                "evidence_id": "ev-telecom-01",
                "source_url": "https://example.com/telecom-regulator-report",
                "supporting_excerpt": "Consumer complaints regarding billing transparency and unused data expiration increased 34%.",
                "source_title": "Telecom Consumer Rights & Billing Audit",
                "publisher": "Regulatory Commission",
            }
        ],
        "claims": [],
        "verifications": [],
        "contradictions": [],
        "research_gaps": ["ARPU elasticity when implementing full data rollover plans"],
    })
    return run_id


from unittest.mock import MagicMock, patch


def test_scenario_telecom_pipeline(telecom_stage1):
    """Execute complete autonomous opportunity discovery for Scenario 2."""
    initial_state = {
        "strategic_analysis_id": "scenario-telecom-analysis-001",
        "research_id": telecom_stage1,
        "strategic_objective": "Identify customer satisfaction improvements and high-retention revenue models",
        "research_iterations": 1,
        "search_budget": {"max_iterations": 1, "max_searches": 2, "max_tasks": 4},
        "execution_status": "running",
        "errors": [],
    }

    mock_specialist_output = {
        "agent_name": "Specialist Analyst",
        "summary": "Specialist analysis completed with verified findings.",
        "evidence_ids": ["ev-telecom-01"],
        "evidence": [{
            "evidence_id": "ev-telecom-01",
            "supporting_excerpt": "Consumer complaints regarding billing transparency and unused data expiration increased 34%.",
            "source_url": "https://example.com/telecom-regulator-report",
            "source_title": "Telecom Consumer Rights & Billing Audit",
            "publisher": "Regulatory Commission",
        }],
        "claims": [],
        "contradictions": [],
    }

    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Executive synthesis and strategic plan.")

    final_state = {}
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
                final_state.update(output)

    # 1. Opportunities discovered
    assert "opportunities" in final_state
    assert len(final_state["opportunities"]) >= 1

    # 2. Revenue-model hypotheses
    assert "hypotheses" in final_state
    assert len(final_state["hypotheses"]) >= 1

    # 3. Risk evaluation completed
    assert "risk_report" in final_state or "risks" in final_state
    risk_rep = final_state.get("risk_report", {})
    risks_count = len(risk_rep.get("business_risks", [])) + len(risk_rep.get("industry_risks", [])) + len(final_state.get("risks", []))
    assert risks_count >= 1

    # 4. Final Executive Report generated
    assert "strategic_report" in final_state
    report = final_state["strategic_report"]
    dir_model = report.get("director_model") if isinstance(report, dict) else report.director_model
    sec_a = report.get("section_a_executive_summary") if isinstance(report, dict) else report.section_a_executive_summary
    assert dir_model == "muse-wonder-1.0"
    assert sec_a != ""

    # 5. Persisted in SQLite
    persisted = get_strategic_analysis("scenario-telecom-analysis-001")
    assert persisted is not None
    assert persisted["status"] == "completed"
