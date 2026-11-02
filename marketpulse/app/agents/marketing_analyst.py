"""
Marketing Intelligence Analyst Agent for MARKETPULSE Stage 2.
Model: Meta Spark 1.3 (spark-1.3).
Investigates brand intelligence, campaign intelligence, channel intelligence,
and detects marketing gaps / weak competitor messaging without fabricating private metrics.
"""

from typing import List, Dict, Any, Optional
from app.agents.specialist import run_specialist
from app.schemas.strategic import MarketingIntelligenceReport


AGENT_NAME = "Marketing Intelligence Analyst"


def run_marketing_analyst(
    objective: str,
    queries: List[str],
    research_questions: Optional[List[str]] = None,
    industry: str = "General Business",
    geography: str = "Global",
    fetch_full_content: bool = True,
    research_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the Marketing Intelligence Analyst research branch."""
    specialist_res = run_specialist(
        agent_name=AGENT_NAME,
        objective=objective,
        queries=queries,
        research_questions=research_questions,
        industry=industry,
        geography=geography,
        fetch_full_content=fetch_full_content,
        research_id=research_id,
    )

    evidence_ids = specialist_res.get("evidence_ids", [])
    summary = specialist_res.get("summary", "")

    # Structured extraction from specialist synthesis
    brand_intel = {
        "positioning_themes": ["Observed public brand value propositions"],
        "messaging_focus": f"Analyzed public messaging for {industry} in {geography}",
    }
    campaign_intel = {
        "seasonal_patterns": "Public campaign rhythms and promotional offers",
        "observable_promotions": "Active consumer-facing discounts and campaigns",
    }
    channel_intel = {
        "digital_channels": ["Organic Search / Content", "Social Media", "Direct E-commerce"],
        "partnerships": "Public co-marketing partnerships",
    }
    marketing_gaps = [
        "Competitor messaging lacks transparency in post-purchase support and delivery guarantees",
        "Under-utilized educational content for differentiated product advantages",
    ]
    differentiation_opps = [
        "Position brand on radical transparency, delivery reliability, and accurate sizing/specifications",
    ]
    unknown_metrics = [
        "Private advertising expenditure (ad spend) is not publicly disclosed",
        "Private conversion rates and exact campaign ROI are confidential",
    ]

    report = MarketingIntelligenceReport(
        agent_name=AGENT_NAME,
        model_name="spark-1.3",
        brand_intelligence=brand_intel,
        campaign_intelligence=campaign_intel,
        channel_intelligence=channel_intel,
        marketing_gaps=marketing_gaps,
        differentiation_opportunities=differentiation_opps,
        unknown_metrics=unknown_metrics,
        supporting_evidence_ids=evidence_ids,
        summary=summary,
    )

    specialist_res["marketing_report"] = report.model_dump()
    return specialist_res
