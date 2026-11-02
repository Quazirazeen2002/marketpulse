"""
Market Intelligence Analyst Agent for MARKETPULSE.
Investigates market structure, market size & growth, industry trends,
supply & demand, regulatory drivers, and emerging business models.
"""

from typing import List, Dict, Any, Optional
from app.agents.specialist import run_specialist


AGENT_NAME = "Market Intelligence Analyst"


def run_market_analyst(
    objective: str,
    queries: List[str],
    research_questions: Optional[List[str]] = None,
    industry: str = "General Business",
    geography: str = "Global",
    fetch_full_content: bool = True,
    research_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the Market Intelligence Analyst research branch."""
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

