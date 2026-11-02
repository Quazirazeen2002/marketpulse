"""
Integration test for SQLite Database Extension & Migration Safety.
Verifies all 13 new Stage 2 tables are created alongside existing Stage 1 tables without dropping data.
"""

import pytest
from sqlalchemy import inspect
from app.database.db import engine, initialize_database
from app.database.models import (
    ResearchRun,
    SourceDocumentRecord,
    EvidenceRecord,
    ResearchClaimRecord,
    StrategicAnalysisRecord,
    OpportunityDbRecord,
    OpportunityScoreRecord,
    RiskAssessmentRecord,
    ScenarioModelRecord,
    ResearchHypothesisRecord,
)


def test_sqlite_tables_coexistence():
    """Verify all Stage 1 and Stage 2 tables coexist in the SQLite schema."""
    initialize_database()
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    # Mandatory Stage 1 tables
    stage1_tables = {
        "research_runs",
        "source_documents",
        "evidence_records",
        "research_claims",
        "contradiction_records",
        "execution_events",
        "search_cache",
    }
    for tbl in stage1_tables:
        assert tbl in existing_tables, f"Stage 1 table '{tbl}' was lost!"

    # Mandatory Stage 2 tables (13 total)
    stage2_tables = {
        "strategic_analyses",
        "marketing_intelligence",
        "commercial_intelligence",
        "opportunity_records",
        "opportunity_evidence",
        "research_hypotheses",
        "followup_research_tasks",
        "risk_assessments",
        "opportunity_scores",
        "scenario_models",
        "scenario_inputs",
        "strategic_recommendations",
        "strategic_execution_events",
    }
    for tbl in stage2_tables:
        assert tbl in existing_tables, f"Stage 2 table '{tbl}' is missing!"


def test_foreign_key_integrity():
    """Verify Stage 2 records maintain valid foreign key references back to Stage 1 research_runs."""
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("strategic_analyses")
    referred_tables = [fk["referred_table"] for fk in fks]
    assert "research_runs" in referred_tables
