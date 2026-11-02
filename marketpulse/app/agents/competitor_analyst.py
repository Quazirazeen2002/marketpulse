"""
Competitor Intelligence Analyst Agent for MARKETPULSE.
Investigates direct/indirect competitors, positioning, product/service offerings,
pricing & promotions, distribution channels, and differentiation opportunities.
"""

from typing import List, Dict, Any, Optional
from app.agents.specialist import run_specialist


AGENT_NAME = "Competitor Intelligence Analyst"


def run_competitor_analyst(
    objective: str,
    queries: List[str],
    research_questions: Optional[List[str]] = None,
    industry: str = "General Business",
    geography: str = "Global",
    fetch_full_content: bool = True,
    research_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the Competitor Intelligence Analyst research branch."""
    return run_specialist(
        agent_name=AGENT_NAME,
        objective=objective,
        queries=queries,
        research_questions=research_questions,
        industry=industry,
        geography=geography,
        fetch_full_content=fetch_full_content,
        research_id=research_id,
    )

