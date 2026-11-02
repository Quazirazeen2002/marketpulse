"""
Integration test for Stage 2 Strategic REST API Endpoints.
Verifies all endpoints return correct status codes, JSON schemas, and error responses.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.database.repository import save_complete_research_run, save_complete_strategic_analysis


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def seeded_research():
    """Ensure a valid Stage 1 run exists for foreign key references."""
    run_id = "test-api-stage1-run"
    save_complete_research_run({
        "research_id": run_id,
        "research_objective": "Test API Objective",
        "industry": "Retail",
        "geography": "Global",
        "time_horizon": "Current",
        "market_report": {},
        "competitor_report": {},
        "customer_report": {},
        "sources": [],
        "evidence_registry": [],
        "claims": [],
        "verifications": [],
        "contradictions": [],
        "research_gaps": [],
    })
    return run_id


def test_start_strategic_analysis_404_on_missing_run(client):
    """Verify POST /api/strategic/analyses returns 404 if Stage 1 research_id doesn't exist."""
    res = client.post(
        "/api/strategic/analyses",
        json={"research_id": "non-existent-run-id-9999"}
    )
    assert res.status_code == 404


def test_start_strategic_analysis_success(client, seeded_research):
    """Verify POST /api/strategic/analyses accepts request with HTTP 202 and returns analysis_id."""
    with patch("app.services.task_manager.task_manager.executor.submit"):
        res = client.post(
            "/api/strategic/analyses",
            json={
                "research_id": seeded_research,
                "strategic_objective": "Discover sizing opportunities",
                "max_research_iterations": 2,
                "max_followup_searches": 3,
                "max_followup_tasks": 6,
            }
        )
    assert res.status_code == 202
    data = res.json()
    assert "analysis_id" in data
    assert data["execution_status"] == "pending"


def test_list_analyses(client):
    """Verify GET /api/strategic/analyses returns list."""
    res = client.get("/api/strategic/analyses")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_scenario_simulation_endpoint(client):
    """Verify POST /api/strategic/opportunities/{id}/simulate calculates unit economics."""
    payload = {
        "scenario_name": "API Test Case",
        "initial_investment": 30000.0,
        "product_selling_price": 80.0,
        "product_cost": 30.0,
        "expected_monthly_orders": 400,
        "monthly_marketing_expenditure": 3000.0,
        "delivery_cost_per_order": 4.0,
        "return_refund_rate": 0.04,
        "fixed_operating_expenses": 5000.0,
        "payment_processing_fee_percent": 0.02,
        "other_variable_cost_per_order": 1.5,
    }

    res = client.post("/api/strategic/opportunities/test-opp-1/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["opportunity_id"] == "test-opp-1"
    assert "base_case" in data
    assert "best_case" in data
    assert "worst_case" in data
    assert data["base_case"]["monthly_revenue"] == 30720.0  # 400 * (1 - 0.04) * 80.0
    assert data["base_case"]["gross_profit"] == 19200.0     # 384 * (80.0 - 30.0)
    assert data["base_case"]["break_even_orders"] > 0
