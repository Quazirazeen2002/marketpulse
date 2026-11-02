"""
Stopping Conditions for Autonomous Research Loop.
Determines whether to continue targeted investigations or terminate the research loop.
"""

from typing import List, Dict, Any, Tuple
from app.schemas.strategic import ResearchHypothesis, HypothesisStatus
from app.services.hypothesis_engine.research_budget import StrategicResearchBudget


def check_stopping_conditions(
    budget: StrategicResearchBudget,
    hypotheses: List[ResearchHypothesis],
    pending_tasks: List[Any],
) -> Tuple[bool, str]:
    """
    Check bounded stopping criteria:
    1. Maximum iteration ceiling reached
    2. Search / task budget exhausted
    3. High-confidence hypothesis saturation (all hypotheses evaluated)
    """
    if not budget.can_iterate():
        return True, f"Ceiling reached: Completed maximum allowed iterations ({budget.max_iterations})."

    if not budget.can_search() and not budget.can_dispatch_task():
        return True, "Ceiling reached: Shared search and follow-up task budget exhausted."

    if not pending_tasks:
        # Check if all hypotheses have reached terminal validation status
        active_hyp = [h for h in hypotheses if h.validation_status in (HypothesisStatus.PROPOSED, HypothesisStatus.INVESTIGATING)]
        if not active_hyp:
            return True, "Confidence reached: All generated hypotheses have been evaluated with empirical evidence."

    return False, "Sufficient budget and unresolved hypotheses exist to continue targeted follow-up research."
