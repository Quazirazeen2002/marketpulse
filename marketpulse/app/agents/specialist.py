"""
Specialist Researcher module for MARKETPULSE.
Performs web search retrieval, full-text acquisition, quality evaluation,
atomic evidence extraction, LLM synthesis, atomic claim extraction,
and research gap identification.
"""

import uuid
from typing import List, Dict, Any, Optional

from app.models.gateway import get_specialist_model, get_research_model
from app.tools.search import search_web

from app.schemas import (
    SourceDocument,
    SourceQualityAssessment,
    EvidenceRecord,
    ResearchClaim,
    ClaimType,
    ClaimStatus,
    SourceAcquisitionStatus,
    SpecialistReport,
    EventType,
)
from app.services.web_search.exceptions import (
    SearchBudgetExceededError,
    EmptySearchResultsError,
    WebSearchError,
    SearchAuthError,
    SearchRateLimitError,
)
from app.services.source_acquisition.engine import acquire_sources_batch
from app.services.evidence_intelligence.source_evaluator import SourceQualityEvaluator
from app.services.evidence_intelligence.evidence_extractor import EvidenceExtractor
from app.services.claim_verification.claim_extractor import ClaimExtractor


def run_specialist(
    agent_name: str,
    objective: str,
    queries: List[str],
    research_questions: Optional[List[str]] = None,
    industry: str = "General Business",
    geography: str = "Global",
    fetch_full_content: bool = True,
    research_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a deep research investigation for a specialist agent:
    1. Search Tavily Search API for each query within research budget.
    2. Acquire full HTML/PDF content or retain snippet-only fallback.
    3. Evaluate source quality across 5 dimensions.
    4. Extract atomic evidence records with exact excerpts and provenance.
    5. Synthesize grounded findings with Spark 1.3.
    6. Extract atomic claims and detect missing data / research gaps.
    """
    emitter = None
    if research_id:
        try:
            from app.graph.nodes import get_emitter_for_run
            emitter = get_emitter_for_run(research_id)
        except Exception:
            emitter = None

    all_raw_results = []
    seen_urls = set()

    # 1. Search operations via Tavily with research budget enforcement
    for query in queries:
        if emitter:
            emitter.emit(
                event_type=EventType.SEARCH_STARTED,
                agent_name=agent_name,
                node_name="search_web",
                message=f"[{agent_name}] Searching Tavily for: '{query}'",
                status="running",
            )

        try:
            results = search_web(query, max_results=5, research_id=research_id)

            if emitter:
                emitter.emit(
                    event_type=EventType.SEARCH_COMPLETED,
                    agent_name=agent_name,
                    node_name="search_web",
                    message=f"[{agent_name}] Tavily retrieved {len(results)} sources for '{query}'.",
                    status="completed",
                )

            for r in results:
                url = r.get("url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                r["query"] = query
                all_raw_results.append(r)

        except EmptySearchResultsError:
            if emitter:
                emitter.emit(
                    event_type=EventType.SEARCH_ZERO_RESULTS,
                    agent_name=agent_name,
                    node_name="search_web",
                    message=f"[{agent_name}] Tavily search completed with 0 results for '{query}'.",
                    status="completed",
                )

        except SearchBudgetExceededError as exc:
            if emitter:
                emitter.emit(
                    event_type=EventType.SEARCH_BUDGET_EXCEEDED,
                    agent_name=agent_name,
                    node_name="search_web",
                    message=f"[{agent_name}] Search budget reached ({exc.max_budget} queries). Skipping further live searches.",
                    status="completed",
                )
            break

        except Exception as exc:
            if emitter:
                emitter.emit(
                    event_type=EventType.SEARCH_FAILED,
                    agent_name=agent_name,
                    node_name="search_web",
                    message=f"[{agent_name}] Tavily search error for '{query}': {exc}",
                    status="failed",
                )
            print(f"[{agent_name}] Query '{query}' search error: {exc}")


    # 2. Source Acquisition (Fetch full text or snippet fallback)
    acquired_sources: List[SourceDocument] = []
    if all_raw_results:
        acquired_sources = acquire_sources_batch(
            all_raw_results,
            max_workers=5 if fetch_full_content else 1,
            fetch_full_content=fetch_full_content,
        )

    # 3. Source Quality Evaluation
    evaluator = SourceQualityEvaluator(industry=industry, geography=geography)
    quality_assessments: Dict[str, SourceQualityAssessment] = {}
    for src in acquired_sources:
        qa = evaluator.evaluate(src, research_objective=objective)
        quality_assessments[src.source_id] = qa

    # 4. Atomic Evidence Extraction
    evidence_extractor = EvidenceExtractor()
    evidence_records: List[EvidenceRecord] = []
    evidence_id_map: Dict[str, EvidenceRecord] = {}

    for src in acquired_sources:
        records = evidence_extractor.extract_from_source(
            src,
            research_questions=research_questions,
            max_evidence_per_source=3,
        )
        for ev in records:
            evidence_records.append(ev)
            evidence_id_map[ev.evidence_id] = ev

    # 5. Model Synthesis with Evidence Grounding (Spark 1.3 for specialist agents)
    model = get_specialist_model()
    summary = ""

    research_gaps = []

    # Map agent name to specialized domain instructions
    domain_guidance = ""
    if "Market" in agent_name:
        domain_guidance = (
            "Focus on: Market structure, market size & growth (ONLY if verified by evidence; if unknown, state unknown), "
            "segmentation, industry trends, supply/demand dynamics, regulatory & economic drivers, and emerging models."
        )
    elif "Competitor" in agent_name:
        domain_guidance = (
            "Focus on: Direct and indirect competitors, competitive positioning, product/service offerings, pricing strategies, "
            "distribution channels, operational strengths, and competitive vulnerabilities."
        )
    elif "Customer" in agent_name:
        domain_guidance = (
            "Focus on: Customer segments, purchasing motivations, pain points, price sensitivity, buying behavior, "
            "unmet needs, and customer complaints or satisfaction trends."
        )
    elif "Marketing" in agent_name:
        domain_guidance = (
            "Focus on: Brand positioning, brand differentiation, messaging, publicly observable advertising campaigns, "
            "seasonal marketing, promotional strategies, channel intelligence (SEO, social, partnerships), weak competitor messaging, "
            "and unexplored marketing channels. NEVER invent private ad spend, conversion rates, impressions, or campaign ROI; "
            "explicitly identify unavailable metrics as unknown."
        )
    elif "Commercial" in agent_name:
        domain_guidance = (
            "Focus on: Product pricing, pricing tiers, subscription models, revenue streams, monetization strategies, "
            "public delivery charges, promotions and discounts, commercial partnerships, pricing gaps, and commercial feasibility. "
            "NEVER invent private financial information; explicitly distinguish public pricing from estimated costs and margins."
        )
    elif "Opportunity" in agent_name:
        domain_guidance = (
            "Focus on: Underserved customer segments, unmet needs, competitor blind spots, weak product offerings, service gaps, "
            "pricing opportunities, new distribution models, and structured opportunity hypotheses backed by evidence."
        )
    elif "Risk" in agent_name:
        domain_guidance = (
            "Focus on: Operational limitations, financial risks, customer adoption barriers, competitive retaliation, market saturation, "
            "regulatory developments, economic disruptions, technology changes, supply-chain risks, and mitigation strategies."
        )

    if model and evidence_records:
        evidence_context_blocks = []
        for ev in evidence_records:
            quality_info = quality_assessments.get(ev.source_id)
            score_str = f"Composite Quality: {quality_info.composite_score:.1f}/100" if quality_info else ""
            evidence_context_blocks.append(
                f"EVIDENCE ID: {ev.evidence_id}\n"
                f"SOURCE: {ev.source_title} ({ev.source_url})\n"
                f"PUBLISHER: {ev.publisher} | QUALITY: {score_str}\n"
                f"EXCERPT: {ev.exact_excerpt}\n"
            )
        evidence_context = "\n---\n".join(evidence_context_blocks)

        prompt = f"""
You are the {agent_name} of MARKETPULSE — an autonomous business intelligence system.

RESEARCH OBJECTIVE:
{objective}

INDUSTRY: {industry} | GEOGRAPHY: {geography}

SPECIALIST GUIDANCE:
{domain_guidance}

VERIFIED RETRIEVED EVIDENCE:
{evidence_context}

INSTRUCTIONS:
1. Synthesize an evidence-backed analysis addressing the research objective.
2. Structure your report into clear analytical findings with specific references to EVIDENCE IDs (e.g., [EV-...]).
3. Distinguish between verified empirical facts and speculative hypotheses.
4. If crucial business figures (such as market size, competitor revenues, or customer numbers) are missing from the evidence, EXPLICITLY state that they are unavailable and list them under 'RESEARCH GAPS'.
5. DO NOT invent facts, market shares, revenue figures, or fake URLs.
6. Acknowledge when evidence comes from snippets rather than full verified articles.

Produce a rigorous, structured analytical brief.
"""
        try:
            response = model.invoke(prompt)
            content = response.content
            if isinstance(content, list):
                summary = "".join(
                    b.get("text", "") for b in content if isinstance(b, dict)
                )
            else:
                summary = str(content)
        except Exception as exc:
            summary = f"Analytical synthesis encountered an error: {exc}"
    elif not model:
        summary = (
            f"Collected {len(evidence_records)} evidence records across {len(acquired_sources)} sources. "
            "Spark 1.3 model is not configured; raw evidence retained."
        )
    else:
        summary = (
            f"No relevant evidence could be retrieved for '{agent_name}'. "
            "Web sources were inaccessible or search yielded no results."
        )

    # 6. Atomic Claim Extraction from Specialist Synthesis
    claim_extractor = ClaimExtractor()
    extracted_claims: List[ResearchClaim] = []
    if summary:
        extracted_claims = claim_extractor.extract_claims(
            text=summary,
            agent_name=agent_name,
            available_evidence_ids=[ev.evidence_id for ev in evidence_records],
        )

    # 7. Identify Research Gaps from Missing Data & Claims
    # Identify gaps if certain core fields are absent
    if "Market" in agent_name:
        has_size_claim = any("market size" in c.claim_text.lower() or "growth" in c.claim_text.lower() for c in extracted_claims)
        if not has_size_claim:
            research_gaps.append(f"No verified market size or CAGR data identified for {industry} in {geography}.")
    elif "Competitor" in agent_name:
        has_pricing_claim = any("price" in c.claim_text.lower() or "cost" in c.claim_text.lower() for c in extracted_claims)
        if not has_pricing_claim:
            research_gaps.append(f"No transparent competitor pricing schedules retrieved for leading players in {geography}.")
    elif "Customer" in agent_name:
        has_demographic_claim = any("demographic" in c.claim_text.lower() or "income" in c.claim_text.lower() for c in extracted_claims)
        if not has_demographic_claim:
            research_gaps.append(f"No quantitative demographic breakdown available for target consumers in {geography}.")

    # Build findings structure for UI compatibility
    findings = []
    for clm in extracted_claims:
        findings.append({
            "finding_id": clm.claim_id,
            "title": f"{clm.claim_type.value.replace('_', ' ').title()}",
            "claim": clm.claim_text,
            "explanation": clm.verification_rationale or f"Extracted from {agent_name} intelligence.",
            "evidence_ids": clm.supporting_evidence_ids,
            "confidence": clm.confidence_score,
            "classification": "evidence_backed" if clm.supporting_evidence_ids else "hypothesis",
            "limitations": [f"Status: {clm.verification_status.value}"] if clm.supporting_evidence_ids else ["Hypothesis: Lacks corroborating evidence"],
        })

    # Prepare evidence dictionaries for state and database
    evidence_dicts = [
        {
            "evidence_id": ev.evidence_id,
            "source_id": ev.source_id,
            "source_url": ev.source_url,
            "source_title": ev.source_title,
            "publisher": ev.publisher,
            "published_at": ev.published_at,
            "supporting_excerpt": ev.exact_excerpt,
            "exact_excerpt": ev.exact_excerpt,
            "page_number": ev.page_number,
            "section_heading": ev.section_heading,
            "source_type": ev.evidence_type,
            "search_provider": getattr(ev, "search_provider", "tavily") or "tavily",
            "extraction_status": getattr(ev, "extraction_status", "snippet_only") or "snippet_only",
            "relevance_score": quality_assessments.get(ev.source_id, SourceQualityAssessment(
                source_id=ev.source_id, credibility_score=50, relevance_score=50, freshness_score=50, completeness_score=50, specificity_score=50, composite_score=50
            )).relevance_score,
            "reliability_score": quality_assessments.get(ev.source_id, SourceQualityAssessment(
                source_id=ev.source_id, credibility_score=50, relevance_score=50, freshness_score=50, completeness_score=50, specificity_score=50, composite_score=50
            )).credibility_score,
            "content_hash": ev.evidence_id,
            "is_cited": ev.is_cited,
            "search_query": ev.search_query,
        }
        for ev in evidence_records
    ]


    return {
        "agent_name": agent_name,
        "research_objective": objective,
        "research_questions": research_questions or [],
        "summary": summary,
        "findings": findings,
        "claims": extracted_claims,
        "evidence_ids": [ev.evidence_id for ev in evidence_records],
        "research_gaps": research_gaps,
        "sources": acquired_sources,
        "source_qualities": quality_assessments,
        "evidence": evidence_dicts,
        "evidence_records": evidence_records,
        "research_status": "completed" if evidence_records else "insufficient_evidence",
    }
