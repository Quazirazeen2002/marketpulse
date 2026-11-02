import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.task_manager import task_manager


@pytest.fixture
def client():
    return TestClient(app)


def test_root_api_gateway_status(client):
    """Verify that root route serves the API gateway status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "MARKETPULSE" in data["service"]
    assert data["status"] == "online"
    assert "frontend" in data


def test_no_obsolete_frontend_dependencies():
    """Verify zero Gradio and zero Jinja2 dependencies in application."""
    import sys
    assert "app.frontend.gradio_app" not in sys.modules
    import app.main
    assert not hasattr(app.main, "gr")
    assert not hasattr(app.main, "demo")
    assert not hasattr(app.main, "templates")


def test_health_endpoints(client):
    """Verify that real health check endpoints return expected keys."""
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
    assert "active_background_tasks" in res_health.json()

    res_meta = client.get("/api/health/meta")
    assert res_meta.status_code == 200
    assert "connected" in res_meta.json()

    res_db = client.get("/api/health/database")
    assert res_db.status_code == 200
    assert res_db.json()["connected"] is True


def test_research_submission_and_progress_flow(client, monkeypatch):
    """Verify research submission returns HTTP 202 and creates progress record."""
    monkeypatch.setattr(task_manager.executor, "submit", lambda fn, *args, **kwargs: None)

    payload = {
        "objective": "Analyze fashion e-commerce trends in Bangladesh",
        "industry": "Fashion & Retail",
        "geography": "Bangladesh",
        "time_horizon": "Current (Real-time)",
        "research_depth": "standard",
    }
    res = client.post("/api/research", json=payload)
    assert res.status_code == 202
    data = res.json()
    assert "research_id" in data
    assert data["execution_status"] == "pending"

    run_id = data["research_id"]

    prog_res = client.get(f"/api/research/{run_id}/progress")
    assert prog_res.status_code == 200
    prog_data = prog_res.json()
    assert prog_data["research_id"] == run_id
    assert "current_stage" in prog_data
    assert "progress_events" in prog_data


def test_reconnection_after_simulated_refresh(client, monkeypatch):
    """Verify that querying progress for a known research ID restores state."""
    monkeypatch.setattr(task_manager.executor, "submit", lambda fn, *args, **kwargs: None)
    t_info = task_manager.submit_research_task(
        objective="Investigate mobile banking in South Asia",
        industry="Fintech",
        geography="South Asia",
    )
    run_id = t_info["research_id"]

    res = client.get(f"/api/research/{run_id}/progress")
    assert res.status_code == 200
    assert res.json()["research_id"] == run_id


def test_agents_directory_endpoint(client):
    """Verify /api/agents returns Director (Muse Wonder) and all specialists (Spark 1.3)."""
    res = client.get("/api/agents")
    assert res.status_code == 200
    agents = res.json()
    assert len(agents) == 4
    agent_by_id = {a["id"]: a for a in agents}

    # Verify Research Director uses muse-wonder-1.0
    assert "director" in agent_by_id
    assert agent_by_id["director"]["name"] == "Research Director"
    assert agent_by_id["director"]["model"] == "muse-wonder-1.0"

    # Verify all specialists use spark-1.3
    specialist_ids = ["market_analyst", "competitor_analyst", "customer_analyst"]
    for s_id in specialist_ids:
        assert s_id in agent_by_id
        assert agent_by_id[s_id]["model"] == "spark-1.3"

    # Verify with all=true returns all 8 agents
    res_all = client.get("/api/agents?all=true")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 8


def test_strategic_api_endpoints(client):
    """Verify strategic analysis endpoints."""
    res = client.get("/api/strategic/opportunities")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    res_hypo = client.get("/api/strategic/hypotheses")
    assert res_hypo.status_code == 200
    assert isinstance(res_hypo.json(), list)

    res_risks = client.get("/api/strategic/risks")
    assert res_risks.status_code == 200
    assert isinstance(res_risks.json(), list)
