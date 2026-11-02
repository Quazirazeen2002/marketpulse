"""
Research Budget and Iteration Guardrails for Autonomous Discovery Engine.
Enforces strict ceilings on iterations, follow-up searches, and task dispatches.
"""

from typing import Dict, Any


DEFAULT_MAX_ITERATIONS = 3
DEFAULT_MAX_FOLLOWUP_SEARCHES = 4
DEFAULT_MAX_FOLLOWUP_TASKS = 8


class StrategicResearchBudget:
    """Tracks and bounds autonomous follow-up exploration per strategic run."""

    def __init__(
        self,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        max_searches: int = DEFAULT_MAX_FOLLOWUP_SEARCHES,
        max_tasks: int = DEFAULT_MAX_FOLLOWUP_TASKS,
    ):
        self.max_iterations = max_iterations
        self.max_searches = max_searches
        self.max_tasks = max_tasks

        self.current_iteration = 0
        self.searches_dispatched = 0
        self.tasks_executed = 0

    def can_iterate(self) -> bool:
        return self.current_iteration < self.max_iterations

    def can_search(self) -> bool:
        return self.searches_dispatched < self.max_searches

    def can_dispatch_task(self) -> bool:
        return self.tasks_executed < self.max_tasks

    def record_iteration(self) -> int:
        self.current_iteration += 1
        return self.current_iteration

    @property
    def searches_conducted(self) -> int:
        return self.searches_dispatched

    def record_search(self, count: int = 1) -> int:
        self.searches_dispatched += count
        return self.searches_dispatched

    def record_task(self, count: int = 1) -> int:
        self.tasks_executed += count
        return self.tasks_executed

    def status_summary(self) -> Dict[str, Any]:
        return {
            "current_iteration": self.current_iteration,
            "max_iterations": self.max_iterations,
            "searches_dispatched": self.searches_dispatched,
            "max_searches": self.max_searches,
            "tasks_executed": self.tasks_executed,
            "max_tasks": self.max_tasks,
            "can_continue": self.can_iterate() and (self.can_search() or self.can_dispatch_task()),
        }
