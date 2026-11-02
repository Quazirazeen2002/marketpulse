"""
Autonomous Hypothesis & Research-Gap Discovery Engine Package.
"""

from app.services.hypothesis_engine.research_budget import StrategicResearchBudget
from app.services.hypothesis_engine.gap_detector import detect_research_gaps
from app.services.hypothesis_engine.hypothesis_generator import generate_hypotheses_from_findings
from app.services.hypothesis_engine.task_prioritizer import prioritize_and_create_tasks
from app.services.hypothesis_engine.hypothesis_validator import validate_hypotheses
from app.services.hypothesis_engine.stopping_conditions import check_stopping_conditions

generate_hypotheses_from_gaps = generate_hypotheses_from_findings
prioritize_followup_tasks = prioritize_and_create_tasks
validate_hypothesis = validate_hypotheses
should_stop_research_loop = check_stopping_conditions

__all__ = [
    "StrategicResearchBudget",
    "detect_research_gaps",
    "generate_hypotheses_from_findings",
    "generate_hypotheses_from_gaps",
    "prioritize_and_create_tasks",
    "prioritize_followup_tasks",
    "validate_hypotheses",
    "validate_hypothesis",
    "check_stopping_conditions",
    "should_stop_research_loop",
]
