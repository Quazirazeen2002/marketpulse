"""
Customer Intelligence Analyst Agent for MARKETPULSE.
Investigates customer segments, preferences, buying motivations, pain points,
price sensitivity, customer complaints, and unmet market needs.
"""

from typing import List, Dict, Any, Optional
from app.agents.specialist import run_specialist


AGENT_NAME = "Customer Intelligence Analyst"


def run_customer_analyst(
    objective: str,
    queries: List[str],
    research_questions: Optional[List[str]] = None,
    industry: str = "General Business",
    geography: str = "Global",
    fetch_full_content: bool = True,
    research_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the Customer Intelligence Analyst research branch."""
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

