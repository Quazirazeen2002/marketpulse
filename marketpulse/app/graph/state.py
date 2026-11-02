from typing import TypedDict, Annotated, List, Dict, Any, Optional
from operator import add


class MarketPulseState(TypedDict, total=False):
    # Core Research Identifiers & Parameters
    research_id: str
    research_objective: str
    industry: str
    geography: str
    time_horizon: str

    # Planning & Question Decomposition
    research_plan: Dict[str, Any]
    research_questions: List[Dict[str, Any]]

    # Specialist Reports
    market_report: Dict[str, Any]
    competitor_report: Dict[str, Any]
    customer_report: Dict[str, Any]

    # Evidence & Source Registry (Accumulated across specialists)
    sources: List[Dict[str, Any]]
    source_qualities: Dict[str, Any]
    evidence_registry: Annotated[List[Dict[str, Any]], add]
    evidence_groups: List[Dict[str, Any]]

    # Claim Verification & Contradiction Records
    claims: List[Dict[str, Any]]
    verifications: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    research_gaps: List[str]

    # Synthesis & Status Dimensions
    status_dimensions: Dict[str, Any]
    final_report: Dict[str, Any]
    research_status: str

    # Observability & Iterations
    iteration_count: int
    errors: List[str]
    execution_events: List[Dict[str, Any]]