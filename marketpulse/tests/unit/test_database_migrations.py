import uuid
from sqlmodel import create_engine, SQLModel, Session, select
from app.database.models import (
    ResearchRun,
    SourceDocumentRecord,
    EvidenceRecord,
    ResearchClaimRecord,
    ContradictionRecordModel,
)
from app.database.repository import compare_runs, get_research_run, list_research_runs


def test_sqlite_schema_and_models():
    """Verify that all new SQLite tables can be created cleanly and queried."""
    test_engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        run_id = f"test_run_{uuid.uuid4().hex[:6]}"
        run = ResearchRun(
            id=run_id,
            objective="Test Database Integrity",
            industry="Testing",
            geography="Global",
            time_horizon="Current",
            status="completed",
            research_quality="strong",
            verification_status="verified",
            total_sources=2,
            verified_claims=1,
        )
        session.add(run)

        source = SourceDocumentRecord(
            source_id="src_db_01",
            research_id=run_id,
            url="https://test.com/doc",
            title="Test Doc",
            extraction_status="retrieved_full_text",
            extracted_text="Sample text content...",
        )
        session.add(source)

        evidence = EvidenceRecord(
            evidence_id="ev_db_01",
            source_id="src_db_01",
            research_id=run_id,
            source_url="https://test.com/doc",
            supporting_excerpt="Sample excerpt",
        )
        session.add(evidence)

        claim = ResearchClaimRecord(
            claim_id="clm_db_01",
            research_id=run_id,
            agent_name="Market Analyst",
            claim_text="Test market assertion",
            verification_status="supported",
            confidence_score=0.9,
        )
        session.add(claim)

        session.commit()

        # Query back
        loaded_run = session.exec(select(ResearchRun).where(ResearchRun.id == run_id)).first()
        assert loaded_run is not None
        assert loaded_run.objective == "Test Database Integrity"
        assert loaded_run.research_quality == "strong"

        loaded_sources = session.exec(select(SourceDocumentRecord).where(SourceDocumentRecord.research_id == run_id)).all()
        assert len(loaded_sources) == 1
        assert loaded_sources[0].url == "https://test.com/doc"
