from sqlmodel import Session, select

from app.database.db import engine, initialize_database
from app.database.models import (
    ResearchRun,
    ResearchAgentRun,
    EvidenceRecord,
)

initialize_database()

with Session(engine) as session:

    research = session.exec(
        select(ResearchRun)
    ).all()

    agents = session.exec(
        select(ResearchAgentRun)
    ).all()

    evidence = session.exec(
        select(EvidenceRecord)
    ).all()

    print("\n=== MARKETPULSE DATABASE ===")

    print("Research sessions:", len(research))
    print("Agent executions:", len(agents))
    print("Evidence records:", len(evidence))

    for item in research:
        print("\nResearch ID:", item.id)
        print("Objective:", item.objective)
        print("Status:", item.status)