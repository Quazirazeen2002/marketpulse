"""
Pydantic Schemas for MARKETPULSE Stage 2 — Strategic Intelligence & Autonomous Opportunity Discovery.
Strict typing, enums, and comprehensive data validation across all strategic models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------
# Strategic Enums
# ---------------------------------------------------------

class HypothesisStatus(str, Enum):
    PROPOSED = "proposed"
    INVESTIGATING = "investigating"
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


class RiskCategory(str, Enum):
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    CUSTOMER_ADOPTION = "customer_adoption"
    COMPETITIVE_RETALIATION = "competitive_retaliation"
    MARKET_SATURATION = "market_saturation"
    REGULATORY = "regulatory"
    ECONOMIC = "economic"
    TECHNOLOGY = "technology"
    SUPPLY_CHAIN = "supply_chain"


class RiskLikelihood(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskImpact(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StrategicEventType(str, Enum):
    STRATEGIC_ANALYSIS_STARTED = "strategic_analysis_started"
    STAGE1_RESEARCH_LOADED = "stage1_research_loaded"
    STRATEGIC_PLANNING_STARTED = "strategic_planning_started"
    SPECIALIST_STARTED = "specialist_started"
    SPECIALIST_COMPLETED = "specialist_completed"
    HYPOTHESIS_GENERATED = "hypothesis_generated"
    RESEARCH_GAP_DETECTED = "research_gap_detected"
    FOLLOWUP_TASK_CREATED = "followup_task_created"
    FOLLOWUP_RESEARCH_STARTED = "followup_research_started"
    FOLLOWUP_RESEARCH_COMPLETED = "followup_research_completed"
    OPPORTUNITY_DISCOVERED = "opportunity_discovered"
    OPPORTUNITY_SCORED = "opportunity_scored"
    RISK_ASSESSMENT_COMPLETED = "risk_assessment_completed"
    SCENARIO_CALCULATED = "scenario_calculated"
    DIRECTOR_REVIEW_STARTED = "director_review_started"
    STRATEGIC_REPORT_GENERATED = "strategic_report_generated"
    STRATEGIC_ANALYSIS_COMPLETED = "strategic_analysis_completed"
    STRATEGIC_ANALYSIS_FAILED = "strategic_analysis_failed"


# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------

class StrategicResearchRequest(BaseModel):
    research_id: str = Field(..., description="Completed Stage 1 research run identifier")
    strategic_objective: Optional[str] = Field(None, description="Optional strategic focus or pivot objective")
    max_research_iterations: int = Field(3, ge=1, le=5)
    max_followup_searches: int = Field(4, ge=1, le=10)
    max_followup_tasks: int = Field(8, ge=1, le=16)


# ---------------------------------------------------------
# Strategic Specialist Reports
# ---------------------------------------------------------

class MarketingIntelligenceReport(BaseModel):
    agent_name: str = "Marketing Intelligence Analyst"
    model_name: str = "spark-1.3"
    brand_intelligence: Dict[str, Any] = Field(default_factory=dict)
    campaign_intelligence: Dict[str, Any] = Field(default_factory=dict)
    channel_intelligence: Dict[str, Any] = Field(default_factory=dict)
    marketing_gaps: List[str] = Field(default_factory=list)
    differentiation_opportunities: List[str] = Field(default_factory=list)
    unknown_metrics: List[str] = Field(default_factory=list, description="Explicitly disclosed unavailable metrics like private ad spend or conversion rates")
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    summary: str = ""


class CommercialIntelligenceReport(BaseModel):
    agent_name: str = "Commercial Intelligence Analyst"
    model_name: str = "spark-1.3"
    pricing_structures: List[Dict[str, Any]] = Field(default_factory=list)
    monetization_models: List[str] = Field(default_factory=list)
    public_delivery_charges: List[Dict[str, Any]] = Field(default_factory=list)
    promotions_and_discounts: List[str] = Field(default_factory=list)
    pricing_gaps: List[str] = Field(default_factory=list)
    commercial_feasibility: str = ""
    distinguished_estimates: List[Dict[str, Any]] = Field(default_factory=list, description="Explicitly marked estimated costs/margins vs public pricing")
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    summary: str = ""


class OpportunityRecord(BaseModel):
    opportunity_id: str
    opportunity_name: str
    problem_statement: str
    target_customer: str
    market_segment: str
    supporting_findings: List[str] = Field(default_factory=list)
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    relevant_competitors: List[str] = Field(default_factory=list)
    proposed_solution: str
    commercial_model: str
    expected_customer_value: str
    competitive_differentiation: str
    potential_barriers: List[str] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    additional_research_required: List[str] = Field(default_factory=list)
    originating_hypothesis_id: Optional[str] = None
    status: str = "discovered"


class OpportunityDiscoveryReport(BaseModel):
    agent_name: str = "Opportunity Discovery Analyst"
    model_name: str = "spark-1.3"
    discovered_opportunities: List[OpportunityRecord] = Field(default_factory=list)
    underserved_segments: List[str] = Field(default_factory=list)
    unmet_needs: List[str] = Field(default_factory=list)
    competitor_blind_spots: List[str] = Field(default_factory=list)
    cross_industry_patterns: List[str] = Field(default_factory=list)
    summary: str = ""


class RiskAssessment(BaseModel):
    risk_id: str
    opportunity_id: Optional[str] = None
    risk_description: str
    risk_category: RiskCategory
    likelihood: RiskLikelihood
    impact: RiskImpact
    likelihood_score: float = Field(0.5, ge=0.0, le=1.0)
    impact_score: float = Field(0.5, ge=0.0, le=1.0)
    evidence_ids: List[str] = Field(default_factory=list)
    mitigation_strategy: str
    residual_risk: str
    missing_information: List[str] = Field(default_factory=list)


class RiskIntelligenceReport(BaseModel):
    agent_name: str = "Risk & Industry Intelligence Analyst"
    model_name: str = "spark-1.3"
    business_risks: List[RiskAssessment] = Field(default_factory=list)
    industry_risks: List[RiskAssessment] = Field(default_factory=list)
    opportunity_risk_matrix: Dict[str, List[RiskAssessment]] = Field(default_factory=dict)
    critical_vulnerabilities: List[str] = Field(default_factory=list)
    summary: str = ""


# ---------------------------------------------------------
# Hypotheses & Follow-up Research
# ---------------------------------------------------------

class ResearchHypothesis(BaseModel):
    hypothesis_id: str
    description: str
    originating_findings: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    validation_status: HypothesisStatus = HypothesisStatus.PROPOSED
    confidence_assessment: float = Field(0.5, ge=0.0, le=1.0)
    follow_up_tasks: List[str] = Field(default_factory=list)
    final_disposition: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)

    @model_validator(mode="before")
    @classmethod
    def handle_confidence_score(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "confidence_score" in data and "confidence_assessment" not in data:
                data["confidence_assessment"] = data.pop("confidence_score")
            elif "confidence_score" in data:
                data.pop("confidence_score")
        return data

    @property
    def confidence_score(self) -> float:
        return self.confidence_assessment

    @confidence_score.setter
    def confidence_score(self, val: float):
        self.confidence_assessment = val


class FollowupResearchTask(BaseModel):
    task_id: str
    hypothesis_id: str
    target_agent: str
    research_question: str
    search_queries: List[str] = Field(default_factory=list)
    priority: int = 1
    status: str = "pending"
    execution_result: Optional[str] = None
    new_evidence_ids: List[str] = Field(default_factory=list)


# ---------------------------------------------------------
# Opportunity Scoring & Ranking
# ---------------------------------------------------------

class OpportunityScore(BaseModel):
    opportunity_id: str
    raw_score: float = Field(..., ge=0.0, le=100.0)
    risk_adjusted_score: float = Field(..., ge=0.0, le=100.0)
    component_scores: Dict[str, float] = Field(default_factory=dict)
    dimension_weights: Dict[str, float] = Field(default_factory=dict)
    scoring_rationale: Dict[str, str] = Field(default_factory=dict)
    evidence_ids: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    uncertainty: str = "moderate"
    scoring_version: str = "2.0-deterministic"


# ---------------------------------------------------------
# Business Scenario Simulation
# ---------------------------------------------------------

class ScenarioInput(BaseModel):
    scenario_name: str = "Base Case"
    initial_investment: float = Field(50000.0, ge=0.0)
    product_selling_price: float = Field(100.0, gt=0.0)
    product_cost: float = Field(40.0, ge=0.0)
    expected_monthly_orders: int = Field(500, ge=0)
    monthly_marketing_expenditure: float = Field(5000.0, ge=0.0)
    delivery_cost_per_order: float = Field(5.0, ge=0.0)
    return_refund_rate: float = Field(0.05, ge=0.0, le=1.0)
    fixed_operating_expenses: float = Field(8000.0, ge=0.0)
    payment_processing_fee_percent: float = Field(0.025, ge=0.0, le=0.5)
    other_variable_cost_per_order: float = Field(2.0, ge=0.0)
    assumptions_rationale: Dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "selling_price" in data and "product_selling_price" not in data:
                data["product_selling_price"] = data.pop("selling_price")
            if "monthly_order_volume" in data and "expected_monthly_orders" not in data:
                data["expected_monthly_orders"] = int(data.pop("monthly_order_volume"))
            if "marketing_expense" in data and "monthly_marketing_expenditure" not in data:
                data["monthly_marketing_expenditure"] = data.pop("marketing_expense")
            if "delivery_cost" in data and "delivery_cost_per_order" not in data:
                data["delivery_cost_per_order"] = data.pop("delivery_cost")
            if "return_rate" in data and "return_refund_rate" not in data:
                data["return_refund_rate"] = data.pop("return_rate")
            if "other_variable_costs" in data and "other_variable_cost_per_order" not in data:
                data["other_variable_cost_per_order"] = data.pop("other_variable_costs")
        return data



class ScenarioResult(BaseModel):
    scenario_name: str
    monthly_revenue: float
    cogs: float
    gross_profit: float
    gross_margin_percent: float
    contribution_per_order: float
    contribution_margin_percent: float
    variable_operating_costs: float
    fixed_operating_costs: float
    total_operating_costs: float
    monthly_operating_profit: float
    annual_operating_profit: float
    break_even_orders: int
    break_even_revenue: float
    estimated_cash_requirement: float
    is_profitable: bool


class SensitivityAnalysis(BaseModel):
    variable_tested: str
    baseline_value: float
    variations: List[Dict[str, Any]] = Field(default_factory=list)


class BusinessScenario(BaseModel):
    opportunity_id: str
    opportunity_name: str
    base_case: ScenarioResult
    best_case: ScenarioResult
    worst_case: ScenarioResult
    sensitivity: List[SensitivityAnalysis] = Field(default_factory=list)
    simulation_notes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------
# Final Strategic Executive Report (Sections A through J)
# ---------------------------------------------------------

class StrategicExecutiveReport(BaseModel):
    strategic_analysis_id: str
    research_id: str
    strategic_objective: str
    industry: str
    geography: str
    generated_at: str = Field(default_factory=utc_now_iso)
    director_model: str = "muse-wonder-1.0"
    specialist_model: str = "spark-1.3"

    # Section A — Executive Summary
    section_a_executive_summary: str
    # Section B — Market Intelligence (Stage 1 reuse + Stage 2 updates)
    section_b_market_intelligence: str
    # Section C — Competitor Intelligence
    section_c_competitor_intelligence: str
    # Section D — Marketing Intelligence
    section_d_marketing_intelligence: str
    # Section E — Commercial Intelligence
    section_e_commercial_intelligence: str
    # Section F — Opportunity Discovery (Ranked)
    section_f_opportunity_discovery: List[Dict[str, Any]] = Field(default_factory=list)
    # Section G — Risk Assessment
    section_g_risk_assessment: List[Dict[str, Any]] = Field(default_factory=list)
    # Section H — Scenario Analysis (Simulated outcomes clearly labeled)
    section_h_scenario_analysis: Optional[Dict[str, Any]] = None
    # Section I — Strategic Recommendations (Evidence-backed vs Hypotheses)
    section_i_strategic_recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    # Section J — Further Research (Unanswered gaps)
    section_j_further_research: List[str] = Field(default_factory=list)

    total_opportunities: int = 0
    total_hypotheses: int = 0
    total_risks: int = 0
    research_iterations_executed: int = 1
    evidence_count: int = 0
