"""
Research Director module (backwards-compatible wrapper).
Imports from research_director.py.
"""

from app.agents.research_director import (
    create_research_plan,
    synthesize_executive_intelligence,
    compute_research_quality_dimensions,
)

__all__ = [
    "create_research_plan",
    "synthesize_executive_intelligence",
    "compute_research_quality_dimensions",
]
