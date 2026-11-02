"""
Task Prioritizer for Autonomous Hypothesis Validation.
Converts research hypotheses into targeted FollowupResearchTask dispatches
assigned to the appropriate specialist agent.
"""

import uuid
from typing import List, Dict, Any
from app.schemas.strategic import ResearchHypothesis, FollowupResearchTask


def prioritize_and_create_tasks(
    hypotheses: List[ResearchHypothesis],
    industry: str = "General Business",
    geography: str = "Global",
    max_tasks: int = 4,
) -> List[FollowupResearchTask]:
    """
    Generate prioritized follow-up research tasks mapped to specific specialist agents.
    """
    tasks: List[FollowupResearchTask] = []

    for hyp in hypotheses:
        if len(tasks) >= max_tasks:
            break

        desc_lower = hyp.description.lower()

        # Map hypothesis focus to target specialist
        if "delivery" in desc_lower or "logistics" in desc_lower or "shipping" in desc_lower:
            tasks.append(FollowupResearchTask(
                task_id=f"TSK-{uuid.uuid4().hex[:6].upper()}",
                hypothesis_id=hyp.hypothesis_id,
                target_agent="Customer Intelligence Analyst",
                research_question=f"Investigate independent customer complaints regarding delivery reliability and courier tracking in {industry} within {geography}.",
                search_queries=[
                    f"{industry} delivery complaints tracking {geography}",
                    f"customer reviews courier delay {industry} {geography}",
                ],
                priority=1,
            ))
            if len(tasks) < max_tasks:
                tasks.append(FollowupResearchTask(
                    task_id=f"TSK-{uuid.uuid4().hex[:6].upper()}",
                    hypothesis_id=hyp.hypothesis_id,
                    target_agent="Commercial Intelligence Analyst",
                    research_question=f"Examine whether competitors in {geography} charge express delivery premiums or offer guaranteed fulfillment tiers.",
                    search_queries=[
                        f"{industry} express shipping delivery fees {geography}",
                        f"competitor delivery policies guarantees {geography}",
                    ],
                    priority=2,
                ))

        elif "sizing" in desc_lower or "fit" in desc_lower or "quality" in desc_lower:
            tasks.append(FollowupResearchTask(
                task_id=f"TSK-{uuid.uuid4().hex[:6].upper()}",
                hypothesis_id=hyp.hypothesis_id,
                target_agent="Competitor Intelligence Analyst",
                research_question=f"Check if leading competitors provide fit guidance tools or standardized sizing charts in {industry} ({geography}).",
                search_queries=[
                    f"{industry} size chart fit guidance {geography}",
                    f"competitor return policy wrong size {geography}",
                ],
                priority=1,
            ))
        else:
            tasks.append(FollowupResearchTask(
                task_id=f"TSK-{uuid.uuid4().hex[:6].upper()}",
                hypothesis_id=hyp.hypothesis_id,
                target_agent="Marketing Intelligence Analyst",
                research_question=f"Investigate how competitors communicate product quality and service reliability in {industry} ({geography}).",
                search_queries=[
                    f"{industry} brand advertising campaigns {geography}",
                    f"{industry} marketing messaging guarantees {geography}",
                ],
                priority=2,
            ))

    return tasks[:max_tasks]
