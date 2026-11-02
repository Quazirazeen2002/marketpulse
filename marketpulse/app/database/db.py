import sqlite3
from sqlmodel import SQLModel, Session, create_engine

from app.config import settings
from app.database.models import (
    ResearchRun,
    ResearchAgentRun,
    SourceDocumentRecord,
    SourceQualityRecord,
    EvidenceRecord,
    ResearchClaimRecord,
    ContradictionRecordModel,
    ExecutionEventRecord,
    ResearchGapRecord,
    ResearchArtifact,
    SearchCacheRecord,
    StrategicAnalysisRecord,
    MarketingIntelligenceRecord,
    CommercialIntelligenceRecord,
    OpportunityDbRecord,
    OpportunityEvidenceLink,
    ResearchHypothesisRecord,
    FollowupResearchTaskRecord,
    RiskAssessmentRecord,
    OpportunityScoreRecord,
    ScenarioModelRecord,
    ScenarioInputRecord,
    StrategicRecommendationRecord,
    StrategicExecutionEventRecord,
)


DATABASE_URL = settings.DATABASE_URL

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)


def run_safe_migrations():
    """Apply safe schema migrations to existing SQLite tables."""
    if not DATABASE_URL.startswith("sqlite"):
        return

    db_path = DATABASE_URL.replace("sqlite:///", "")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        def add_col(table, col, col_def):
            cols = [c[1] for c in cursor.execute(f"PRAGMA table_info({table});").fetchall()]
            if col not in cols:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_def};")

        # Check research_runs
        tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        if "research_runs" in tables:
            add_col("research_runs", "research_quality", "TEXT DEFAULT 'moderate'")
            add_col("research_runs", "verification_status", "TEXT DEFAULT 'partially_verified'")
            add_col("research_runs", "total_sources", "INTEGER DEFAULT 0")
            add_col("research_runs", "full_text_sources", "INTEGER DEFAULT 0")
            add_col("research_runs", "snippet_only_sources", "INTEGER DEFAULT 0")
            add_col("research_runs", "verified_claims", "INTEGER DEFAULT 0")
            add_col("research_runs", "unverified_claims", "INTEGER DEFAULT 0")
            add_col("research_runs", "contradictions_count", "INTEGER DEFAULT 0")
            add_col("research_runs", "completed_at", "TIMESTAMP NULL")

        if "evidence_records" in tables:
            add_col("evidence_records", "source_id", "TEXT NULL")
            add_col("evidence_records", "duplicate_group_id", "TEXT NULL")
            add_col("evidence_records", "search_provider", "TEXT DEFAULT 'tavily'")
            add_col("evidence_records", "extraction_status", "TEXT DEFAULT 'snippet_only'")

        if "source_documents" in tables:
            add_col("source_documents", "search_provider", "TEXT DEFAULT 'tavily'")

        conn.commit()
        conn.close()
    except Exception as exc:
        print(f"[MIGRATION NOTICE] {exc}")


def initialize_database():
    """Create all SQLModel tables safely without dropping existing data and run migrations."""
    SQLModel.metadata.create_all(engine)
    run_safe_migrations()


def get_db_session():
    """Context manager providing an independent Session."""
    return Session(engine)


def get_session():
    """Provide a database session generator for FastAPI dependencies."""
    with Session(engine) as session:
        yield session



def save_research(state: dict):
    """
    Backwards-compatible wrapper that invokes the full repository save.
    """
    from app.database.repository import save_complete_research_run
    return save_complete_research_run(state)
