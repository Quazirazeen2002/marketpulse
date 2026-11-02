"""
Scenario 3 — Food Delivery Platforms & Merchant Opportunity Discovery.
Prompt: "Investigate food delivery platforms and identify underserved merchant or customer needs that could create new commercial opportunities."
Validates:
- Competitor comparison
- Customer pain-point research
- Commercial opportunities
- Marketing gaps
- Risk assessments
- Scenario simulation (Base, Best, Worst + Sensitivity)
"""

import pytest
from app.graph.strategic_workflow import strategic_graph
from app.database.repository import save_complete_research_run, get_strategic_analysis, get_stored_scenarios
from app.services.business_simulation import generate_scenario_suite, ScenarioInput


@pytest.fixture
def food_delivery_stage1():
    """Seed Stage 1 Food Delivery Research Run."""
    run_id = "scenario-food-delivery-stage1"
    save_complete_research_run({
        "research_id": run_id,
        "research_objective": "Investigate food delivery platforms and identify underserved merchant or customer needs.",
        "industry": "Food Delivery Platforms",
        "geography": "Urban Hubs",
        "time_horizon": "Current",
        "market_report": {
            "market_structure": "Two major platforms control 85% of urban deliveries.",
            "cagr": "12.0%",
            "key_drivers": ["Urbanization", "Cloud kitchen growth", "Digital wallets"],
            "summary": "Platform duopoly with high commission pressure on independent restaurants.",
        },
        "competitor_report": {
            "direct_competitors": ["Platform Alpha", "Platform Beta"],
            "pricing": "25-30% restaurant commission + variable customer delivery fee",
            "summary": "Aggressive discount voucher wars eroding restaurant operating margins.",
        },
        "customer_report": {
            "unmet_needs": ["Affordable single-meal portions without exorbitant delivery fees", "Consistent hot food temperature"],
            "complaints": ["Small order surcharges exceed food price", "Rider delays during rush hours"],
            "summary": "Single-diner segment severely underserved due to flat delivery fees.",
        },
        "sources": [
            {
                "url": "https://example.com/restaurant-industry-survey",
                "title": "Merchant Commission & Delivery Economics Survey",
                "publisher": "Hospitality Insight",
                "full_text": "Independent restaurants report 28% commission rates make off-peak food delivery unprofitable.",
                "quality_score": 0.92,
            }
        ],
        "evidence_registry": [
            {
                "evidence_id": "ev-food-01",
                "source_url": "https://example.com/restaurant-industry-survey",
                "supporting_excerpt": "Independent restaurants report 28% commission rates make off-peak food delivery unprofitable.",
                "source_title": "Merchant Commission & Delivery Economics Survey",
                "publisher": "Hospitality Insight",
            }
        ],
        "claims": [],
        "verifications": [],
        "contradictions": [],
        "research_gaps": ["Customer willingness to batch lunch orders within office buildings"],
    })
    return run_id


from unittest.mock import MagicMock, patch


def test_scenario_food_delivery_pipeline_with_simulation(food_delivery_stage1):
    """Execute complete autonomous opportunity discovery and financial scenario simulation."""
    initial_state = {
        "strategic_analysis_id": "scenario-food-analysis-001",
        "research_id": food_delivery_stage1,
        "strategic_objective": "Discover underserved merchant and single-diner delivery opportunities",
        "research_iterations": 1,
        "search_budget": {"max_iterations": 1, "max_searches": 2, "max_tasks": 4},
        "execution_status": "running",
        "errors": [],
    }

    mock_specialist_output = {
        "agent_name": "Specialist Analyst",
        "summary": "Specialist analysis completed with verified findings.",
        "evidence_ids": ["ev-food-01"],
        "evidence": [{
            "evidence_id": "ev-food-01",
            "supporting_excerpt": "Independent restaurants report 28% commission rates make off-peak food delivery unprofitable.",
            "source_url": "https://example.com/restaurant-industry-survey",
            "source_title": "Merchant Commission & Delivery Economics Survey",
            "publisher": "Hospitality Insight",
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

    # 2. Risk assessment
    assert "risk_report" in final_state or "risks" in final_state
    risk_rep = final_state.get("risk_report", {})
    risks_count = len(risk_rep.get("business_risks", [])) + len(risk_rep.get("industry_risks", [])) + len(final_state.get("risks", []))
    assert risks_count >= 1

    # 3. Financial simulation verification for the top opportunity
    sim_input = ScenarioInput(
        scenario_name="Office Building Lunch Batching",
        initial_investment=25000.0,
        product_selling_price=12.0,  # $12 average meal
        product_cost=6.50,          # Wholesale meal prep
        expected_monthly_orders=2000,
        monthly_marketing_expenditure=2000.0,
        delivery_cost_per_order=1.50,  # Batched building drop-off
        return_refund_rate=0.0,
        fixed_operating_expenses=4000.0,
        payment_processing_fee_percent=0.02,
        other_variable_cost_per_order=0.50,
    )

    suite = generate_scenario_suite(sim_input)
    assert suite["base_case"].monthly_revenue == 24000.0
    assert suite["base_case"].gross_profit > 0
    assert suite["base_case"].is_profitable is True
    assert suite["base_case"].break_even_orders < 2000

    # 4. Final Executive Report generated
    assert "strategic_report" in final_state
    report = final_state["strategic_report"]
    dir_model = report.get("director_model") if isinstance(report, dict) else report.director_model
    sec_a = report.get("section_a_executive_summary") if isinstance(report, dict) else report.section_a_executive_summary
    assert dir_model == "muse-wonder-1.0"
    assert sec_a != ""
