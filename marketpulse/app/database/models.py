from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, Text


def utc_now():
    return datetime.now(timezone.utc)


class ResearchRun(SQLModel, table=True):
    __tablename__ = "research_runs"

    id: str = Field(primary_key=True, index=True)
    objective: str = Field(sa_type=Text)
    industry: str = Field(index=True)
    geography: str = Field(index=True)
    time_horizon: str
    status: str = Field(default="planning", index=True)
    research_quality: str = Field(default="moderate", index=True)
    verification_status: str = Field(default="partially_verified", index=True)

    total_sources: int = 0
    full_text_sources: int = 0
    snippet_only_sources: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradictions_count: int = 0

    research_plan: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    final_report: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    created_at: datetime = Field(default_factory=utc_now)
    completed_at: Optional[datetime] = None


class ResearchAgentRun(SQLModel, table=True):
    __tablename__ = "research_agent_runs"

    id: Optional[int] = Field(default=None, primary_key=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    agent_name: str = Field(index=True)
    status: str = "completed"
    summary: str = Field(default="", sa_type=Text)
    evidence_count: int = 0
    created_at: datetime = Field(default_factory=utc_now)


class SourceDocumentRecord(SQLModel, table=True):
    __tablename__ = "source_documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: str = Field(index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    url: str = Field(sa_type=Text)
    canonical_url: Optional[str] = None
    title: str = Field(default="")
    publisher: str = Field(default="")
    author: Optional[str] = None
    publication_date: Optional[str] = None
    extraction_status: str = Field(default="snippet_only")
    extracted_text: str = Field(default="", sa_type=Text)
    content_hash: str = Field(default="")
    content_type: str = Field(default="text/html")
    duplicate_group_id: Optional[str] = None
    is_canonical: bool = True
    http_status: Optional[int] = None
    search_provider: str = Field(default="tavily")
    created_at: datetime = Field(default_factory=utc_now)


class SourceQualityRecord(SQLModel, table=True):
    __tablename__ = "source_quality_assessments"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: str = Field(index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    credibility_score: float = 0.0
    relevance_score: float = 0.0
    freshness_score: float = 0.0
    completeness_score: float = 0.0
    specificity_score: float = 0.0
    composite_score: float = 0.0
    scoring_rationale: str = Field(default="", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)


class EvidenceRecord(SQLModel, table=True):
    __tablename__ = "evidence_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    evidence_id: str = Field(index=True)
    source_id: Optional[str] = Field(default=None, index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    is_cited: bool = False
    search_query: str = Field(default="", sa_type=Text)
    source_url: str = Field(sa_type=Text)
    source_title: str = Field(default="")
    publisher: str = Field(default="")
    published_at: Optional[str] = None
    collected_at: datetime = Field(default_factory=utc_now)
    supporting_excerpt: str = Field(default="", sa_type=Text)
    source_type: str = "tavily_search"
    search_provider: str = Field(default="tavily")
    extraction_status: str = Field(default="snippet_only")
    relevance_score: float = 0.0
    reliability_score: float = 0.0
    content_hash: str = ""
    duplicate_group_id: Optional[str] = None


class SearchCacheRecord(SQLModel, table=True):
    __tablename__ = "search_cache"

    id: Optional[int] = Field(default=None, primary_key=True)
    cache_key: str = Field(index=True, unique=True)
    query: str = Field(sa_type=Text)
    search_depth: str = "basic"
    topic: str = "general"
    filters_hash: str = ""
    results: list = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )
    result_count: int = 0
    search_provider: str = "tavily"
    created_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime = Field(index=True)



class ResearchClaimRecord(SQLModel, table=True):
    __tablename__ = "research_claims"

    id: Optional[int] = Field(default=None, primary_key=True)
    claim_id: str = Field(index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    agent_name: str = Field(index=True)
    claim_text: str = Field(sa_type=Text)
    claim_type: str = "fact"
    verification_status: str = "unverified"
    confidence_score: float = 0.0
    verification_rationale: str = Field(default="", sa_type=Text)
    is_hypothesis: bool = False
    created_at: datetime = Field(default_factory=utc_now)


class ContradictionRecordModel(SQLModel, table=True):
    __tablename__ = "contradiction_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    contradiction_id: str = Field(index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    topic: str = "Operations & Strategy"
    claim_a_id: str
    claim_a_text: str = Field(sa_type=Text)
    claim_b_id: str
    claim_b_text: str = Field(sa_type=Text)
    conflict_summary: str = Field(sa_type=Text)
    resolution_status: str = "unresolved"
    created_at: datetime = Field(default_factory=utc_now)


class ExecutionEventRecord(SQLModel, table=True):
    __tablename__ = "execution_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(index=True)
    run_id: str = Field(foreign_key="research_runs.id", index=True)
    agent_name: str
    node_name: str
    event_type: str
    status: str
    message: str = Field(sa_type=Text)
    timestamp: datetime = Field(default_factory=utc_now)
    duration_ms: Optional[int] = None


class ResearchGapRecord(SQLModel, table=True):
    __tablename__ = "research_gaps"

    id: Optional[int] = Field(default=None, primary_key=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    gap_description: str = Field(sa_type=Text)
    agent_name: str = "Research Director"
    created_at: datetime = Field(default_factory=utc_now)


class ResearchArtifact(SQLModel, table=True):
    __tablename__ = "research_artifacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    agent_name: str
    artifact_type: str
    content: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(default_factory=utc_now)


# ---------------------------------------------------------
# STAGE 2 STRATEGIC INTELLIGENCE MODELS (13 New Tables)
# ---------------------------------------------------------

class StrategicAnalysisRecord(SQLModel, table=True):
    __tablename__ = "strategic_analyses"

    id: str = Field(primary_key=True, index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    strategic_objective: str = Field(sa_type=Text)
    status: str = Field(default="planning", index=True)
    research_iterations: int = 1
    total_hypotheses: int = 0
    total_opportunities: int = 0
    total_risks: int = 0
    strategic_plan: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    final_report: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)
    completed_at: Optional[datetime] = None


class MarketingIntelligenceRecord(SQLModel, table=True):
    __tablename__ = "marketing_intelligence"

    id: Optional[int] = Field(default=None, primary_key=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    brand_intelligence: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    campaign_intelligence: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    channel_intelligence: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    marketing_gaps: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    summary: str = Field(default="", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)


class CommercialIntelligenceRecord(SQLModel, table=True):
    __tablename__ = "commercial_intelligence"

    id: Optional[int] = Field(default=None, primary_key=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    pricing_structures: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    monetization_models: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    public_delivery_charges: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    pricing_gaps: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    commercial_feasibility: str = Field(default="", sa_type=Text)
    summary: str = Field(default="", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)


class OpportunityDbRecord(SQLModel, table=True):
    __tablename__ = "opportunity_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: str = Field(index=True, unique=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    opportunity_name: str = Field(index=True)
    problem_statement: str = Field(sa_type=Text)
    target_customer: str = Field(default="")
    market_segment: str = Field(default="")
    proposed_solution: str = Field(sa_type=Text)
    commercial_model: str = Field(sa_type=Text)
    expected_customer_value: str = Field(default="", sa_type=Text)
    competitive_differentiation: str = Field(default="", sa_type=Text)
    originating_hypothesis_id: Optional[str] = None
    status: str = Field(default="discovered", index=True)
    created_at: datetime = Field(default_factory=utc_now)


class OpportunityEvidenceLink(SQLModel, table=True):
    __tablename__ = "opportunity_evidence"

    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: str = Field(index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    evidence_id: str = Field(index=True)
    is_supporting: bool = True
    created_at: datetime = Field(default_factory=utc_now)


class ResearchHypothesisRecord(SQLModel, table=True):
    __tablename__ = "research_hypotheses"

    id: Optional[int] = Field(default=None, primary_key=True)
    hypothesis_id: str = Field(index=True, unique=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    description: str = Field(sa_type=Text)
    validation_status: str = Field(default="proposed", index=True)
    confidence_assessment: float = 0.5
    final_disposition: Optional[str] = Field(default=None, sa_type=Text)
    originating_findings: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class FollowupResearchTaskRecord(SQLModel, table=True):
    __tablename__ = "followup_research_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: str = Field(index=True, unique=True)
    hypothesis_id: str = Field(index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    target_agent: str = Field(index=True)
    research_question: str = Field(sa_type=Text)
    priority: int = 1
    status: str = Field(default="pending", index=True)
    execution_result: Optional[str] = Field(default=None, sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)


class RiskAssessmentRecord(SQLModel, table=True):
    __tablename__ = "risk_assessments"

    id: Optional[int] = Field(default=None, primary_key=True)
    risk_id: str = Field(index=True, unique=True)
    opportunity_id: Optional[str] = Field(default=None, index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    risk_description: str = Field(sa_type=Text)
    risk_category: str = Field(index=True)
    likelihood: str = "medium"
    impact: str = "medium"
    likelihood_score: float = 0.5
    impact_score: float = 0.5
    mitigation_strategy: str = Field(default="", sa_type=Text)
    residual_risk: str = Field(default="", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)


class OpportunityScoreRecord(SQLModel, table=True):
    __tablename__ = "opportunity_scores"

    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: str = Field(index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    raw_score: float = 0.0
    risk_adjusted_score: float = 0.0
    component_scores: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    dimension_weights: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    scoring_rationale: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    scoring_version: str = "2.0-deterministic"
    created_at: datetime = Field(default_factory=utc_now)


class ScenarioModelRecord(SQLModel, table=True):
    __tablename__ = "scenario_models"

    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: str = Field(index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    scenario_name: str = Field(default="Base Case", index=True)
    monthly_revenue: float = 0.0
    gross_profit: float = 0.0
    gross_margin_percent: float = 0.0
    contribution_margin_percent: float = 0.0
    monthly_operating_profit: float = 0.0
    annual_operating_profit: float = 0.0
    break_even_orders: int = 0
    break_even_revenue: float = 0.0
    estimated_cash_requirement: float = 0.0
    is_profitable: bool = False
    created_at: datetime = Field(default_factory=utc_now)


class ScenarioInputRecord(SQLModel, table=True):
    __tablename__ = "scenario_inputs"

    id: Optional[int] = Field(default=None, primary_key=True)
    opportunity_id: str = Field(index=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    scenario_name: str = Field(default="Base Case")
    input_parameters: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)


class StrategicRecommendationRecord(SQLModel, table=True):
    __tablename__ = "strategic_recommendations"

    id: Optional[int] = Field(default=None, primary_key=True)
    strategic_analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    title: str = Field(default="")
    description: str = Field(sa_type=Text)
    category: str = Field(default="evidence_backed", index=True)  # evidence_backed, hypothesis, validation_required
    supporting_evidence_ids: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=utc_now)


class StrategicExecutionEventRecord(SQLModel, table=True):
    __tablename__ = "strategic_execution_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(index=True)
    analysis_id: str = Field(foreign_key="strategic_analyses.id", index=True)
    research_id: str = Field(foreign_key="research_runs.id", index=True)
    agent_name: str
    node_name: str
    event_type: str = Field(index=True)
    status: str
    message: str = Field(sa_type=Text)
    timestamp: datetime = Field(default_factory=utc_now)
    duration_ms: Optional[int] = None
