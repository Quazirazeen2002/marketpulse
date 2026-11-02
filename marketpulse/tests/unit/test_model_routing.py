"""
Unit tests for MARKETPULSE Multi-Model Routing Architecture:
- Research Director exclusively uses Meta Muse Wonder (muse-wonder-1.0).
- All specialist agents (Market, Competitor, Customer) exclusively use Spark 1.3 (spark-1.3).
"""

from unittest.mock import patch, MagicMock
from app.config import settings
from app.models.gateway import (
    get_director_model,
    get_specialist_model,
    get_research_model,
    director_model_available,
    specialist_model_available,
)


def test_director_model_uses_muse_wonder():
    """Verify that get_director_model configures Meta Muse Wonder (muse-wonder-1.0)."""
    with patch.object(settings, "META_API_KEY", "test_key"), \
         patch.object(settings, "META_BASE_URL", "https://api.meta.ai/v1"), \
         patch.object(settings, "META_MUSE_WONDER_MODEL", "muse-wonder-1.0"):
        model = get_director_model()
        assert model is not None
        assert model.model_name == "muse-wonder-1.0"


def test_specialist_model_uses_spark():
    """Verify that get_specialist_model configures Spark 1.3 (spark-1.3)."""
    with patch.object(settings, "META_API_KEY", "test_key"), \
         patch.object(settings, "META_BASE_URL", "https://api.meta.ai/v1"), \
         patch.object(settings, "META_SPARK_MODEL", "spark-1.3"):
        model = get_specialist_model()
        assert model is not None
        assert model.model_name == "spark-1.3"


def test_get_research_model_routing():
    """Verify routing logic maps director to Muse Wonder and all other agents to Spark 1.3."""
    with patch.object(settings, "META_API_KEY", "test_key"), \
         patch.object(settings, "META_BASE_URL", "https://api.meta.ai/v1"), \
         patch.object(settings, "META_MUSE_WONDER_MODEL", "muse-wonder-1.0"), \
         patch.object(settings, "META_SPARK_MODEL", "spark-1.3"):

        director_model = get_research_model("director")
        assert director_model is not None
        assert director_model.model_name == "muse-wonder-1.0"

        research_director_model = get_research_model("Research Director")
        assert research_director_model is not None
        assert research_director_model.model_name == "muse-wonder-1.0"

        # Specialists must use spark-1.3
        for role in ["market", "market_analyst", "competitor", "competitor_analyst", "customer", "customer_analyst", "specialist"]:
            spec_model = get_research_model(role)
            assert spec_model is not None
            assert spec_model.model_name == "spark-1.3", f"Agent role '{role}' did not route to spark-1.3"


def test_model_unconfigured_fallback():
    """Verify that models gracefully return None when credentials are unconfigured."""
    with patch.object(settings, "META_API_KEY", ""):
        assert get_director_model() is None
        assert get_specialist_model() is None
        assert director_model_available() is False
        assert specialist_model_available() is False


def test_director_agent_invokes_director_model():
    """Verify that Research Director calls get_director_model during planning and synthesis."""
    from app.agents.research_director import create_research_plan, synthesize_executive_intelligence

    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Executive brief output")

    with patch("app.agents.research_director.get_director_model", return_value=mock_model) as mock_get:
        # 1. create_research_plan
        plan = create_research_plan(
            objective="Analyze test industry",
            industry="Tech",
            geography="Global",
            time_horizon="Current",
        )
        assert mock_get.called
        assert len(plan["research_questions"]) > 0

    with patch("app.agents.research_director.get_director_model", return_value=mock_model) as mock_get:
        # 2. synthesize_executive_intelligence
        report = synthesize_executive_intelligence(
            research_id="test_run_123",
            objective="Analyze test industry",
            industry="Tech",
            geography="Global",
            specialist_reports={},
            sources=[],
            evidence=[],
            claims=[],
            contradictions=[],
            research_gaps=[],
        )
        assert mock_get.called
        assert "executive_report" in report


def test_specialist_agent_invokes_specialist_model():
    """Verify that Specialist agents call get_specialist_model during synthesis with retrieved evidence."""
    from app.agents.specialist import run_specialist

    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Specialist analysis output with findings.")

    mock_search_results = [
        {
            "evidence_id": "EV-TEST1",
            "url": "https://example.com/market-report",
            "title": "Market Report",
            "content": "The market grew by 15 percent year over year.",
            "publisher": "example.com",
            "score": 0.95,
            "query": "test query",
            "search_provider": "tavily",
            "source_type": "tavily_search",
        }
    ]

    with patch("app.agents.specialist.get_specialist_model", return_value=mock_model) as mock_get, \
         patch("app.agents.specialist.search_web", return_value=mock_search_results), \
         patch("app.agents.specialist.acquire_sources_batch") as mock_acquire:
        
        from app.schemas import SourceDocument, SourceAcquisitionStatus
        mock_acquire.return_value = [
            SourceDocument(
                source_id="SRC-TEST1",
                url="https://example.com/market-report",
                title="Market Report",
                extracted_text="The market grew by 15 percent year over year in Q3 2026.",
                raw_content="The market grew by 15 percent year over year in Q3 2026.",
                clean_content="The market grew by 15 percent year over year in Q3 2026.",
                acquisition_status=SourceAcquisitionStatus.SNIPPET_ONLY,
                publisher="example.com",
                search_provider="tavily",
            )
        ]

        res = run_specialist(
            agent_name="Market Intelligence Analyst",
            objective="Analyze test market",
            queries=["test query"],
        )
        assert mock_get.called
        assert "summary" in res
        assert mock_model.invoke.called
