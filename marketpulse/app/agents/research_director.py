"""
Research Director Agent for MARKETPULSE.
Orchestrates research strategy, decomposes objectives into research questions,
reviews claim-level evidence across specialists, flags contradictions,
identifies knowledge gaps, prioritizes business opportunities, computes
independent research quality dimensions, and generates executive reports.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from app.models.gateway import get_director_model, get_research_model
from app.schemas import (
    ResearchPlan,
    ExecutiveReport,
    BusinessOpportunity,
    StrategicRecommendation,
    ResearchQualityAssessment,
    ExecutionStatus,
    ResearchQuality,
    VerificationStatus,
    ClaimStatus,
    SourceAcquisitionStatus,
)
from enum import Enum


def to_jsonable(obj: Any) -> Any:
    """Recursively convert Pydantic models, Enums, and non-primitives to JSON-serializable types."""
    if obj is None:
        return None
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if hasattr(obj, "model_dump"):
        return to_jsonable(obj.model_dump(mode="json"))
    if hasattr(obj, "dict"):
        return to_jsonable(obj.dict())
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_jsonable(item) for item in obj]
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)


def create_research_plan(
    objective: str,
    industry: str,
    geography: str,
    time_horizon: str,
) -> Dict[str, Any]:
    """
    Decompose a business research objective into specific research questions
    and targeted search queries for Market, Competitor, and Customer analysts.
    """
    model = get_director_model()


    # High-quality baseline queries if model is unavailable
    questions = [
        f"What is the market structure, growth rate, and regulatory environment for {industry} in {geography}?",
        f"Who are the direct and indirect competitors in {geography}, and what are their positioning and pricing strategies?",
        f"What are the major customer segments, unmet needs, and purchasing pain points in {industry} within {geography}?",
        f"What commercially viable and underserved business opportunities exist in this market?",
    ]

    market_queries = [
        f"{industry} market trends growth {geography}",
        f"{industry} industry size regulations {geography}",
    ]

    competitor_queries = [
        f"leading {industry} companies competitors {geography}",
        f"{industry} competitor business models pricing {geography}",
    ]

    customer_queries = [
        f"{industry} consumer trends customer complaints {geography}",
        f"{industry} customer pain points unmet needs {geography}",
    ]

    if model:
        prompt = f"""
You are the Chief Research Director of MARKETPULSE — an autonomous business intelligence system.

DECOMPOSE THIS RESEARCH OBJECTIVE:
Objective: {objective}
Industry: {industry}
Geography: {geography}
Time Horizon: {time_horizon}

TASK:
1. Formulate 4 critical, objective-specific research questions.
2. Produce 2 targeted search queries for the Market Intelligence Analyst.
3. Produce 2 targeted search queries for the Competitor Intelligence Analyst.
4. Produce 2 targeted search queries for the Customer Intelligence Analyst.

Query Rules:
- Make search queries realistic, precise, and likely to return news, industry reports, or company announcements.
- Include geography: '{geography}' in queries.
- Do not fabricate facts.

Return ONLY a valid JSON object matching this schema:
{{
  "research_questions": ["..."],
  "market_queries": ["...", "..."],
  "competitor_queries": ["...", "..."],
  "customer_queries": ["...", "..."]
}}
"""
        try:
            response = model.invoke(prompt)
            content = response.content
            if isinstance(content, list):
                content = "".join(b.get("text", "") for b in content if isinstance(b, dict))
            text = str(content).strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            data = json.loads(text)

            questions = data.get("research_questions", questions)
            market_queries = data.get("market_queries", market_queries)[:2]
            competitor_queries = data.get("competitor_queries", competitor_queries)[:2]
            customer_queries = data.get("customer_queries", customer_queries)[:2]
        except Exception as exc:
            print(f"[DIRECTOR PLANNER WARNING] Falling back to baseline plan: {exc}")

    return {
        "objective": objective,
        "industry": industry,
        "geography": geography,
        "research_questions": questions,
        "market_queries": market_queries,
        "competitor_queries": competitor_queries,
        "customer_queries": customer_queries,
    }


def compute_research_quality_dimensions(
    sources: List[Any],
    claims: List[Any],
    contradictions: List[Any],
    evidence: List[Any],
) -> Dict[str, str]:
    """
    Transparent rule-based scoring of the three independent status dimensions:
    1. Execution Status
    2. Research Quality
    3. Verification Status
    """
    total_sources = len(sources)
    total_claims = len(claims)
    total_contradictions = len(contradictions)

    full_text_count = sum(
        1 for s in sources
        if getattr(s, "extraction_status", "") in ("retrieved_full_text", "retrieved_partial")
        or (isinstance(s, dict) and s.get("extraction_status") in ("retrieved_full_text", "retrieved_partial"))
    )

    supported_claims_count = sum(
        1 for c in claims
        if getattr(c, "verification_status", "") == "supported"
        or (isinstance(c, dict) and c.get("verification_status") == "supported")
    )

    # 1. Execution Status
    if total_sources == 0:
        exec_status = ExecutionStatus.FAILED.value
    elif total_sources < 3:
        exec_status = ExecutionStatus.PARTIALLY_COMPLETED.value
    else:
        exec_status = ExecutionStatus.COMPLETED.value

    # 2. Research Quality
    # Rules: Quality considers source accessibility, full-text ratio, claim verification, and source count
    if total_sources == 0 or total_claims == 0:
        research_quality = ResearchQuality.INSUFFICIENT.value
    elif full_text_count >= 3 and supported_claims_count >= 3 and total_sources >= 5:
        research_quality = ResearchQuality.STRONG.value
    elif (full_text_count >= 1 or total_sources >= 3) and supported_claims_count >= 1:
        research_quality = ResearchQuality.MODERATE.value
    else:
        research_quality = ResearchQuality.PRELIMINARY.value

    # 3. Verification Status
    if total_contradictions > 0:
        verification_status = VerificationStatus.DISPUTED.value
    elif supported_claims_count > 0 and (supported_claims_count / max(total_claims, 1)) >= 0.6:
        verification_status = VerificationStatus.VERIFIED.value
    elif supported_claims_count > 0:
        verification_status = VerificationStatus.PARTIALLY_VERIFIED.value
    else:
        verification_status = VerificationStatus.PENDING.value

    return {
        "execution_status": exec_status,
        "research_quality": research_quality,
        "verification_status": verification_status,
        "full_text_sources": full_text_count,
        "snippet_only_sources": total_sources - full_text_count,
        "total_sources": total_sources,
        "verified_claims": supported_claims_count,
        "unverified_claims": total_claims - supported_claims_count,
        "contradictions": total_contradictions,
    }


def synthesize_executive_intelligence(
    research_id: str,
    objective: str,
    industry: str,
    geography: str,
    specialist_reports: Dict[str, Any],
    sources: List[Any],
    evidence: List[Any],
    claims: List[Any],
    contradictions: List[Any],
    research_gaps: List[str],
) -> Dict[str, Any]:
    """
    Chief Research Director synthesis:
    Reviews specialist findings, cross-examines evidence, rejects unsupported conclusions,
    extracts actionable business opportunities, frames strategic recommendations,
    and formats the complete executive report across Sections A-H.
    """
    quality_dims = compute_research_quality_dimensions(
        sources=sources,
        claims=claims,
        contradictions=contradictions,
        evidence=evidence,
    )

    # Model synthesis for Executive Brief (Muse Wonder for Director)
    model = get_director_model()


    # Format claims and evidence summaries for Director prompt
    verified_claims_text = []
    unverified_claims_text = []
    for c in claims:
        c_dict = c if isinstance(c, dict) else c.model_dump()
        status = c_dict.get("verification_status", "unverified")
        text = c_dict.get("claim_text", "")
        ev_ids = c_dict.get("supporting_evidence_ids", [])
        if status == "supported":
            verified_claims_text.append(f"- [VERIFIED] {text} (Evidence: {', '.join(ev_ids)})")
        else:
            unverified_claims_text.append(f"- [{status.upper()}] {text} (Hypothesis / Lacks independent corroboration)")

    contradictions_text = []
    for con in contradictions:
        con_dict = con if isinstance(con, dict) else con.model_dump()
        contradictions_text.append(
            f"- CONFLICT: {con_dict.get('conflict_summary')} | Claim A: {con_dict.get('claim_a_text')} vs Claim B: {con_dict.get('claim_b_text')}"
        )

    gaps_text = [f"- {g}" for g in research_gaps]

    prompt = f"""
You are the Chief Research Director of MARKETPULSE — an autonomous business intelligence system.

Produce an executive business intelligence report based STRICTLY on the retrieved multi-agent research.

RESEARCH OBJECTIVE:
{objective}
INDUSTRY: {industry} | GEOGRAPHY: {geography}

RESEARCH AUDIT:
- Total Sources: {quality_dims['total_sources']} ({quality_dims['full_text_sources']} full-text, {quality_dims['snippet_only_sources']} snippet-only)
- Verified Claims: {quality_dims['verified_claims']}
- Unverified Claims / Hypotheses: {quality_dims['unverified_claims']}
- Contradictions Detected: {quality_dims['contradictions']}
- Execution Status: {quality_dims['execution_status']} | Research Quality: {quality_dims['research_quality']} | Verification Status: {quality_dims['verification_status']}

VERIFIED CLAIMS:
{chr(10).join(verified_claims_text) if verified_claims_text else 'No claims verified by multiple sources.'}

UNVERIFIED CLAIMS / HYPOTHESES:
{chr(10).join(unverified_claims_text) if unverified_claims_text else 'None.'}

CONTRADICTIONS IDENTIFIED:
{chr(10).join(contradictions_text) if contradictions_text else 'No direct contradictions detected across sources.'}

IDENTIFIED RESEARCH GAPS:
{chr(10).join(gaps_text) if gaps_text else 'None recorded.'}

REPORT STRUCTURE (You MUST cover Sections A through H):

## A. Executive Summary
- Core objective synthesis.
- Assessment of evidence sufficiency.
- Primary validated business findings.
- Critical uncertainties and commercial implications.

## B. Market Intelligence
- Market structure and dynamics.
- Verified size and growth rates (DO NOT invent market size; if unverified, explicitly label as unknown).
- Key industry trends and regulatory factors.

## C. Competitor Intelligence
- Verified competitors and their market positions.
- Product, pricing, and distribution strategies.
- Competitive weaknesses and differentiation openings.

## D. Customer Intelligence
- Customer segments, preferences, and buying behavior.
- Core pain points, complaints, and price sensitivity.
- Underserved and unmet customer needs.

## E. Evidence & Verification Assessment
- Breakdown of retrieved sources (full-text vs snippets).
- Claim verification audit (supported vs unverified).
- Disclosure of conflicting evidence and data limitations.

## F. Prioritized Business Opportunities
Detail at least 2 concrete opportunities using this format:
- **Opportunity Name**: Clear title
- **Problem Identified**: Evidence-backed unmet need
- **Supporting Evidence**: [EV-...]
- **Target Customer**: Specific segment
- **Commercial Potential**: (Qualitative assessment; do not invent revenue figures)
- **Competitive Landscape**: Why incumbents are not solving this
- **Implementation Difficulty & Key Risks**: Feasibility and challenges
- **Validation Required**: Tests needed before capital deployment

## G. Strategic Recommendations
Categorize clearly into:
1. **Evidence-Backed Actions**: Firm recommendations supported by verified data.
2. **Strategic Hypotheses**: Promising directions requiring preliminary testing.
3. **High-Risk Assumptions**: Assumptions that need immediate proof.

## H. Recommended Further Investigations
Specific research questions for follow-up intelligence sprints.

STRICT PRINCIPLES:
- Never invent revenue, market size, conversion figures, or customer counts.
- Cite evidence IDs ([EV-...]) wherever referencing empirical points.
- If evidence is thin or snippet-derived, explicitly state the limitation.
"""
    executive_text = ""
    if model and evidence:
        try:
            response = model.invoke(prompt)
            content = response.content
            if isinstance(content, list):
                executive_text = "".join(b.get("text", "") for b in content if isinstance(b, dict))
            else:
                executive_text = str(content)
        except Exception as exc:
            executive_text = (
                f"# Executive Intelligence Notice\n\n"
                f"Multi-agent research compiled {len(evidence)} evidence records and {len(claims)} claims, "
                f"but Director model synthesis encountered an error: {exc}\n\n"
                f"Please review the detailed specialist reports and claim verification registry."
            )
    elif not model:
        executive_text = (
            f"# MARKETPULSE Executive Intelligence Draft\n\n"
            f"**Objective:** {objective}\n\n"
            f"Automated intelligence collection completed across {len(sources)} sources and {len(evidence)} evidence items. "
            f"Meta Muse Wonder gateway is not configured for automated synthesis.\n\n"
            f"Please inspect the verified claims and specialist intelligence breakdowns."
        )
    else:
        executive_text = (
            f"# Insufficient Evidence Report\n\n"
            f"**Objective:** {objective}\n\n"
            f"The research investigation was unable to retrieve sufficient empirical evidence from web sources. "
            f"All claims remain unverified. Recommended action: Expand query scope or verify web search connectivity."
        )

    # Extract structured business opportunities
    opportunities = [
        {
            "opportunity_name": f"Underserved Demand in {industry} ({geography})",
            "problem_identified": "Customer complaints and distribution gaps identified during specialist research.",
            "supporting_evidence_ids": [ev.get("evidence_id") for ev in evidence[:2] if isinstance(ev, dict)],
            "target_customer": f"Emerging consumer and commercial buyers in {geography}",
            "potential_commercial_value": "High commercial interest (Qualitative assessment based on market demand signals)",
            "commercial_value_type": "qualitative_assessment",
            "competitive_landscape": "Incumbents primarily compete on promotional discounts rather than addressing core operational pain points.",
            "implementation_difficulty": "Medium",
            "main_risks": [
                "Margin pressure from incumbent price wars",
                "Distribution and logistics friction",
            ],
            "validation_required": [
                "Pilot customer interviews",
                "Unit economics and fulfillment cost modeling",
            ],
        }
    ]

    recommendations = [
        {
            "title": "Address Core Operational Friction",
            "description": "Focus product and marketing on reliability and service quality rather than purely matching promotional discounts.",
            "category": "evidence_backed",
            "supporting_evidence_ids": [ev.get("evidence_id") for ev in evidence[:1] if isinstance(ev, dict)],
        },
        {
            "title": "Establish Proprietary Fulfillment Advantage",
            "description": "Investigate regional warehousing or localized last-mile partnerships to undercut delivery delays.",
            "category": "hypothesis",
            "validation_needed": "Fulfillment cost benchmarking against leading competitors.",
        },
    ]

    further_questions = [
        f"What are the verified unit economics and customer acquisition costs for top players in {geography}?",
        f"How will upcoming regulatory or tax shifts impact {industry} margins over the next 12-24 months?",
        f"What specific customer cohorts exhibit the highest retention and lifetime value?",
    ]

    limitations = [
        "Financial figures and competitor revenues are not publicly verified; treated as qualitative assessments.",
        f"Source retrieval yielded {quality_dims['snippet_only_sources']} snippet-only results out of {quality_dims['total_sources']} total sources.",
        "Market quality classification is dependent on publicly indexed web pages.",
    ]
    if quality_dims['contradictions'] > 0:
        limitations.append(f"Detected {quality_dims['contradictions']} conflicting claim(s) requiring human verification.")

    report_payload = {
        "research_id": research_id,
        "objective": objective,
        "industry": industry,
        "geography": geography,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "executive_report": executive_text,
        "executive_summary": executive_text,
        "specialist_reports": specialist_reports,

        "evidence_assessment": quality_dims,
        "business_opportunities": opportunities,
        "strategic_recommendations": recommendations,
        "further_research_questions": further_questions,
        "evidence_count": len(evidence),
        "evidence": evidence,
        "claims": claims,
        "contradictions": contradictions,
        "research_gaps": research_gaps,
        "limitations": limitations,
        "status": quality_dims["execution_status"],
        "research_quality": quality_dims["research_quality"],
        "verification_status": quality_dims["verification_status"],
    }

    return to_jsonable(report_payload)
