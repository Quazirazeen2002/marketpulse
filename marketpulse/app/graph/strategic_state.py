"""
StrategicState Schema for MARKETPULSE Stage 2 LangGraph Orchestration.
Defines typed state channels and reducers for parallel specialist execution,
bounded hypothesis exploration, and strategic report synthesis.
"""

from typing import TypedDict, List, Dict, Any, Optional
import operator


class StrategicState(TypedDict, total=False):
    # Core Identifiers
    strategic_analysis_id: str
    research_id: str
    strategic_objective: str
    industry: str
    geography: str

    # Stage 1 Ingested Intelligence
    stage1_findings: Dict[str, Any]
    stage1_evidence_ids: List[str]
    evidence_records: List[Dict[str, Any]]
    claims: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]

    # Specialist Reports
    market_report: Dict[str, Any]
    competitor_report: Dict[str, Any]
    customer_report: Dict[str, Any]
    marketing_report: Dict[str, Any]
    commercial_report: Dict[str, Any]
    opportunity_report: Dict[str, Any]
    risk_report: Dict[str, Any]

    # Autonomous Discovery & Hypotheses
    hypotheses: List[Dict[str, Any]]
    followup_tasks: List[Dict[str, Any]]
    followup_results: List[Dict[str, Any]]
    research_iterations: int
    search_budget: Dict[str, Any]
    research_gaps: List[str]

    # Scoring & Scenarios
    opportunity_scores: Dict[str, Any]
    opportunities: List[Dict[str, Any]]
    scenario_models: Dict[str, Any]
    strategic_recommendations: List[Dict[str, Any]]

    # Executive Output & Telemetry
    execution_status: str
    research_quality: str
    strategic_report: Dict[str, Any]
    execution_events: List[Dict[str, Any]]
    errors: List[str]
