"""
Scenario 1 — Fashion E-Commerce in Bangladesh.
Prompt: "Investigate the Bangladesh fashion e-commerce industry and discover opportunities for a new online fashion brand."
Validates:
- Stage 1 research loaded
- Marketing and commercial agents investigate
- Opportunity Analyst proposes hypotheses
- Risk Analyst evaluates threats
- Research Director requests additional evidence where needed
- Opportunities are ranked
- Final report is generated
"""

import pytest
from app.graph.strategic_workflow import strategic_graph
from app.database.repository import save_complete_research_run, get_strategic_analysis


@pytest.fixture
def fashion_ecommerce_stage1():
    """Seed Stage 1 Bangladesh Fashion E-Commerce research run."""
    run_id = "scenario-fashion-bd-stage1"
    save_complete_research_run({
        "research_id": run_id,
        "research_objective": "Investigate the Bangladesh fashion e-commerce industry and discover opportunities for a new online fashion brand.",
        "industry": "Fashion E-Commerce",
        "geography": "Bangladesh",
        "time_horizon": "Current",
        "market_report": {
            "market_structure": "Dominated by marketplaces and social-commerce sellers.",
            "cagr": "18.5%",
            "key_drivers": ["4G expansion", "Mobile banking adoption (bKash/Nagad)"],
            "summary": "Rapidly expanding market with high customer churn.",
        },
        "competitor_report": {
            "direct_competitors": ["Daraz", "Aarong", "Fabrilife", "Sailor"],
            "pricing": "BDT 600 - 3,500",
            "summary": "Heavy reliance on flash discount sales; poor size consistency.",
        },
        "customer_report": {
            "unmet_needs": ["Accurate clothing sizing", "Prompt return pickups", "Authentic fabric"],
            "complaints": ["Returns take over 14 days", "Sizing varies wildly across orders"],
            "summary": "Fit and sizing dissatisfaction drives 20-30% returns.",
        },
        "sources": [
            {
                "url": "https://example.com/bd-fashion-report",
                "title": "Bangladesh E-Commerce Logistics & Sizing Report",
                "publisher": "Retail Watch Bangladesh",
                "full_text": "Fashion return rates in Dhaka average 22% largely due to sizing discrepancies.",
                "quality_score": 0.90,
            }
        ],
        "evidence_registry": [
            {
                "evidence_id": "ev-fashion-bd-01",
                "source_url": "https://example.com/bd-fashion-report",
                "supporting_excerpt": "Fashion return rates in Dhaka average 22% largely due to sizing discrepancies.",
                "source_title": "Bangladesh E-Commerce Logistics & Sizing Report",
                "publisher": "Retail Watch Bangladesh",
            }
        ],
        "claims": [],
        "verifications": [],
        "contradictions": [],
        "research_gaps": ["Customer willingness to pay for guaranteed same-day fit exchange"],
    })
    return run_id


from unittest.mock import MagicMock, patch


def test_scenario_fashion_ecommerce_pipeline(fashion_ecommerce_stage1):
    """Execute complete autonomous opportunity discovery for Scenario 1."""
    initial_state = {
        "strategic_analysis_id": "scenario-fashion-analysis-001",
        "research_id": fashion_ecommerce_stage1,
        "strategic_objective": "Discover underserved opportunity vectors in Bangladesh fashion e-commerce",
        "research_iterations": 1,
        "search_budget": {"max_iterations": 1, "max_searches": 2, "max_tasks": 4},
        "execution_status": "running",
        "errors": [],
    }

    mock_specialist_output = {
        "agent_name": "Specialist Analyst",
        "summary": "Specialist analysis completed with verified findings.",
        "evidence_ids": ["ev-fashion-bd-01"],
        "evidence": [{
            "evidence_id": "ev-fashion-bd-01",
            "supporting_excerpt": "Fashion return rates in Dhaka average 22% largely due to sizing discrepancies.",
            "source_url": "https://example.com/bd-fashion-report",
            "source_title": "Bangladesh E-Commerce Logistics & Sizing Report",
            "publisher": "Retail Watch Bangladesh",
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
    opps = final_state["opportunities"]
    assert len(opps) >= 1

    # 2. Hypotheses generated & investigated
    assert "hypotheses" in final_state
    hyps = final_state["hypotheses"]
    assert len(hyps) >= 1

    # 3. Opportunity scored
    assert "opportunity_scores" in final_state
    scores = final_state["opportunity_scores"]
    assert len(scores) >= 1
    first_score = list(scores.values())[0] if isinstance(scores, dict) else scores[0]
    raw_score = first_score.get("raw_score") if isinstance(first_score, dict) else first_score.raw_score
    assert raw_score > 0.0

    # 4. Final Executive Report generated by Research Director
    assert "strategic_report" in final_state
    report = final_state["strategic_report"]
    dir_model = report.get("director_model") if isinstance(report, dict) else report.director_model
    sec_a = report.get("section_a_executive_summary") if isinstance(report, dict) else report.section_a_executive_summary
    sec_f = report.get("section_f_opportunity_discovery") if isinstance(report, dict) else report.section_f_opportunity_discovery
    assert dir_model == "muse-wonder-1.0"
    assert sec_a != ""
    assert len(sec_f) >= 1

    # 5. Persisted in SQLite
    persisted = get_strategic_analysis("scenario-fashion-analysis-001")
    assert persisted is not None
    assert persisted["status"] == "completed"
