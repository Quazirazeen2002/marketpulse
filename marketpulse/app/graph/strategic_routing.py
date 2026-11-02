"""
Conditional Routing Logic for Stage 2 Strategic LangGraph Workflow.
Enforces bounded research loops and conditional follow-up investigation branching.
"""

from app.graph.strategic_state import StrategicState
from app.schemas.strategic import HypothesisStatus


def should_execute_followup(state: StrategicState) -> str:
    """
    Decide whether to execute targeted follow-up research or proceed to scoring.
    """
    tasks = state.get("followup_tasks", [])
    hypotheses = state.get("hypotheses", [])
    current_iter = state.get("research_iterations", 1)
    budget = state.get("search_budget", {})
    max_iter = budget.get("max_iterations", 3) if isinstance(budget, dict) else 3

    if current_iter >= max_iter:
        return "opportunity_scoring"

    has_active_hypotheses = any(
        (getattr(h, "validation_status", None) in ("investigating", "proposed", HypothesisStatus.INVESTIGATING, HypothesisStatus.PROPOSED)
         or (isinstance(h, dict) and h.get("validation_status") in ("investigating", "proposed")))
        for h in hypotheses
    )

    if (tasks or has_active_hypotheses) and current_iter < max_iter:
        return "followup_investigation"

    return "opportunity_scoring"
