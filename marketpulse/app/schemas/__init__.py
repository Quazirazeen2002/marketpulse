from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------
# Status Enums
# ---------------------------------------------------------

class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIALLY_COMPLETED = "partially_completed"
    FAILED = "failed"


class ResearchQuality(str, Enum):
    INSUFFICIENT = "insufficient"
    PRELIMINARY = "preliminary"
    MODERATE = "moderate"
    STRONG = "strong"


class VerificationStatus(str, Enum):
    PENDING = "pending"
    PARTIALLY_VERIFIED = "partially_verified"
    VERIFIED = "verified"
    DISPUTED = "disputed"


class SourceAcquisitionStatus(str, Enum):
    RETRIEVED_FULL_TEXT = "retrieved_full_text"
    RETRIEVED_PARTIAL = "retrieved_partial"
    SNIPPET_ONLY = "snippet_only"
    INACCESSIBLE = "inaccessible"
    UNSUPPORTED_FORMAT = "unsupported_format"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    EXTRACTION_FAILED = "extraction_failed"


class ClaimStatus(str, Enum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    CONTRADICTED = "contradicted"
    UNVERIFIED = "unverified"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class ClaimType(str, Enum):
    FACT = "fact"
    MARKET_STRUCTURE = "market_structure"
    COMPETITOR_STRATEGY = "competitor_strategy"
    CUSTOMER_BEHAVIOR = "customer_behavior"
    COMMERCIAL_OPPORTUNITY = "commercial_opportunity"
    RISK_ASSESSMENT = "risk_assessment"
    HYPOTHESIS = "hypothesis"


class EventType(str, Enum):
    RESEARCH_STARTED = "research_started"
    RESEARCH_QUESTIONS_CREATED = "research_questions_created"
    SPECIALIST_STARTED = "specialist_started"
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    SEARCH_ZERO_RESULTS = "search_zero_results"
    SEARCH_FAILED = "search_failed"
    SEARCH_CACHED_REUSED = "search_cached_reused"
    SEARCH_BUDGET_EXCEEDED = "search_budget_exceeded"
    SOURCE_RETRIEVAL_STARTED = "source_retrieval_started"
    SOURCE_RETRIEVAL_COMPLETED = "source_retrieval_completed"
    SOURCE_QUALITY_ASSESSED = "source_quality_assessed"
    EVIDENCE_EXTRACTED = "evidence_extracted"
    DUPLICATE_DETECTED = "duplicate_detected"
    CLAIM_EXTRACTED = "claim_extracted"
    CLAIM_VERIFICATION_STARTED = "claim_verification_started"
    CLAIM_VERIFIED = "claim_verified"
    CONTRADICTION_DETECTED = "contradiction_detected"
    DIRECTOR_REVIEW_STARTED = "director_review_started"
    REPORT_GENERATED = "report_generated"
    RESEARCH_COMPLETED = "research_completed"
    RESEARCH_FAILED = "research_failed"



# ---------------------------------------------------------
# Request & Questions
# ---------------------------------------------------------

class ResearchRequest(BaseModel):
    objective: str
    industry: str = "General Business"
    geography: str = "Global"
    time_horizon: str = "Current"
    max_search_queries_per_agent: int = 2
    fetch_full_content: bool = True


class ResearchQuestion(BaseModel):
    question_id: str
    agent_target: str
    question_text: str
    search_queries: List[str] = Field(default_factory=list)


class ResearchPlan(BaseModel):
    objective: str
    industry: str
    geography: str
    research_questions: List[str] = Field(default_factory=list)
    market_queries: List[str] = Field(default_factory=list)
    competitor_queries: List[str] = Field(default_factory=list)
    customer_queries: List[str] = Field(default_factory=list)


# ---------------------------------------------------------
# Search & Source Documents
# ---------------------------------------------------------

class SearchResult(BaseModel):
    evidence_id: str
    title: str
    url: str
    content: str = ""
    engine: str = "tavily"
    publisher: str = ""
    score: float = 0.0
    published_date: Optional[str] = None
    query: str = ""
    is_cited: bool = False
    search_provider: str = "tavily"
    source_type: str = "tavily_search"


class SourceDocument(BaseModel):
    source_id: str
    url: str
    canonical_url: Optional[str] = None
    title: str = "Untitled"
    publisher: str = "Unknown"
    author: Optional[str] = None
    publication_date: Optional[str] = None
    retrieved_at: str = Field(default_factory=utc_now_iso)
    extraction_status: SourceAcquisitionStatus = SourceAcquisitionStatus.SNIPPET_ONLY
    extracted_text: str = ""
    content_hash: str = ""
    content_type: str = "text/html"
    page_count: Optional[int] = None
    duplicate_group_id: Optional[str] = None
    is_canonical: bool = True
    http_status: Optional[int] = None
    error_message: Optional[str] = None
    search_provider: str = "tavily"


class SourceQualityAssessment(BaseModel):
    source_id: str
    credibility_score: float = Field(ge=0, le=100)
    relevance_score: float = Field(ge=0, le=100)
    freshness_score: float = Field(ge=0, le=100)
    completeness_score: float = Field(ge=0, le=100)
    specificity_score: float = Field(ge=0, le=100)
    composite_score: float = Field(ge=0, le=100)
    scoring_rationale: str = ""
    evaluation_version: str = "1.0.0"
    is_snippet_only: bool = False


# ---------------------------------------------------------
# Evidence & Claims
# ---------------------------------------------------------

class EvidenceRecord(BaseModel):
    evidence_id: str
    source_id: str
    research_question_id: Optional[str] = None
    source_url: str
    source_title: str
    publisher: str = ""
    published_at: Optional[str] = None
    collected_at: str = Field(default_factory=utc_now_iso)
    exact_excerpt: str
    normalized_statement: str = ""
    page_number: Optional[int] = None
    section_heading: Optional[str] = None
    evidence_type: str = "tavily_search"
    search_provider: str = "tavily"
    extraction_status: str = "snippet_only"
    extraction_quality: str = "high"
    confidence_score: float = 0.8
    is_cited: bool = False
    search_query: str = ""
    duplicate_group_id: Optional[str] = None



class EvidenceGroup(BaseModel):
    group_id: str
    canonical_source_id: str
    canonical_url: str
    duplicate_source_ids: List[str] = Field(default_factory=list)
    similarity_score: float = 1.0
    detection_method: str = "exact_hash"


class ResearchClaim(BaseModel):
    claim_id: str
    agent_name: str
    claim_text: str
    claim_type: ClaimType = ClaimType.FACT
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    verification_status: ClaimStatus = ClaimStatus.UNVERIFIED
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    verification_rationale: str = ""
    is_hypothesis: bool = False


class ClaimVerification(BaseModel):
    verification_id: str
    claim_id: str
    status: ClaimStatus
    supporting_sources_count: int = 0
    contradicting_sources_count: int = 0
    independent_sources_count: int = 0
    confidence_score: float
    confidence_rationale: str
    verified_at: str = Field(default_factory=utc_now_iso)


class ContradictionRecord(BaseModel):
    contradiction_id: str
    topic: str
    claim_a_id: str
    claim_a_text: str
    evidence_a_ids: List[str] = Field(default_factory=list)
    claim_b_id: str
    claim_b_text: str
    evidence_b_ids: List[str] = Field(default_factory=list)
    conflict_summary: str
    resolution_status: str = "unresolved"
    director_assessment: Optional[str] = None


# ---------------------------------------------------------
# Opportunities & Recommendations
# ---------------------------------------------------------

class BusinessOpportunity(BaseModel):
    opportunity_name: str
    problem_identified: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    target_customer: str
    potential_commercial_value: str
    commercial_value_type: str = "qualitative_assessment"
    competitive_landscape: str
    implementation_difficulty: str = "Medium"
    main_risks: List[str] = Field(default_factory=list)
    validation_required: List[str] = Field(default_factory=list)


class StrategicRecommendation(BaseModel):
    title: str
    description: str
    category: str = "evidence_backed"
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    validation_needed: Optional[str] = None


# ---------------------------------------------------------
# Specialist & Executive Reports
# ---------------------------------------------------------

class SpecialistReport(BaseModel):
    agent_name: str
    research_objective: str
    research_questions: List[str] = Field(default_factory=list)
    summary: str
    claims: List[ResearchClaim] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    research_gaps: List[str] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
    research_status: str = "completed"


class ExecutiveReport(BaseModel):
    research_id: str
    objective: str
    industry: str
    geography: str
    generated_at: str = Field(default_factory=utc_now_iso)
    executive_summary: str
    market_intelligence: str
    competitor_intelligence: str
    customer_intelligence: str
    evidence_assessment: Dict[str, Any] = Field(default_factory=dict)
    business_opportunities: List[BusinessOpportunity] = Field(default_factory=list)
    strategic_recommendations: List[StrategicRecommendation] = Field(default_factory=list)
    further_research_questions: List[str] = Field(default_factory=list)
    specialist_reports: Dict[str, Any] = Field(default_factory=dict)
    evidence_count: int = 0
    full_text_count: int = 0
    snippet_only_count: int = 0
    verified_claims_count: int = 0
    unverified_claims_count: int = 0
    contradictions_count: int = 0
    research_gaps: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    execution_status: ExecutionStatus = ExecutionStatus.COMPLETED
    research_quality: ResearchQuality = ResearchQuality.MODERATE
    verification_status: VerificationStatus = VerificationStatus.PARTIALLY_VERIFIED


class ResearchQualityAssessment(BaseModel):
    run_id: str
    execution_status: ExecutionStatus
    research_quality: ResearchQuality
    verification_status: VerificationStatus
    total_sources: int = 0
    full_text_sources: int = 0
    snippet_only_sources: int = 0
    source_quality_avg: float = 0.0
    total_claims: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    contradictions: int = 0
    coverage_ratio: float = 0.0
    rationale: List[str] = Field(default_factory=list)


class ExecutionEvent(BaseModel):
    event_id: str
    run_id: str
    timestamp: str = Field(default_factory=utc_now_iso)
    agent_name: str
    node_name: str
    event_type: EventType
    status: str
    message: str
    entity_ids: List[str] = Field(default_factory=list)
    duration_ms: Optional[int] = None


# Stage 2 Strategic Schemas
from app.schemas.strategic import (
    HypothesisStatus,
    RiskCategory,
    RiskLikelihood,
    RiskImpact,
    StrategicEventType,
    StrategicResearchRequest,
    MarketingIntelligenceReport,
    CommercialIntelligenceReport,
    OpportunityRecord,
    OpportunityDiscoveryReport,
    RiskAssessment,
    RiskIntelligenceReport,
    ResearchHypothesis,
    FollowupResearchTask,
    OpportunityScore,
    ScenarioInput,
    ScenarioResult,
    SensitivityAnalysis,
    BusinessScenario,
    StrategicExecutiveReport,
)
