from pydantic import BaseModel, Field
from typing import Optional

from app.schemas import (
    ResearchClaim,
    SourceDocument,
    EvidenceRecord as SchemaEvidenceRecord,
    SpecialistReport as NewSpecialistReport,
    ExecutiveReport,
    ExecutionStatus,
    ResearchQuality,
    VerificationStatus,
)

class ResearchFinding(BaseModel):

    finding_id: str

    title: str

    claim: str
    explanation: str

    evidence_ids: list[str] = Field(default_factory=list)

    confidence: float = Field(
        ge=0,
        le=1
    )

    classification: str = "evidence_lead"

    limitations: list[str] = Field(
        default_factory=list
    )


class SpecialistReport(BaseModel):

    agent_name: str

    research_objective: str

    summary: str

    findings: list[ResearchFinding] = Field(
        default_factory=list
    )

    evidence_ids: list[str] = Field(
        default_factory=list
    )

    research_status: str = "completed"


class ResearchPlan(BaseModel):

    objective: str

    industry: str

    geography: str
    
    research_questions: list[str]

    market_queries: list[str]

    competitor_queries: list[str]

    customer_queries: list[str]

    

