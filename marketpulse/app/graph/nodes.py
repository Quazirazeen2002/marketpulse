"""
LangGraph Node implementations for MARKETPULSE Stage 1.
Implements request validation, research question decomposition,
parallel specialist research branches, cross-agent synthesis,
deduplication, claim verification, contradiction detection,
director executive review, and persistence.
"""

import time
import uuid
from typing import Dict, Any, List

from app.graph.state import MarketPulseState
from app.agents.market_analyst import run_market_analyst
from app.agents.competitor_analyst import run_competitor_analyst
from app.agents.customer_analyst import run_customer_analyst
from app.agents.research_director import (
    create_research_plan,
    synthesize_executive_intelligence,
    compute_research_quality_dimensions,
)
from app.services.evidence_intelligence.deduplication import cluster_sources_and_evidence
from app.services.claim_verification.claim_verifier import verify_claims_against_evidence
from app.services.claim_verification.contradiction_detector import detect_contradictions
from app.services.claim_verification.citation_validator import validate_citations_and_traceability
from app.database.repository import save_complete_research_run, save_execution_event
from app.observability.events import ExecutionEventEmitter
from app.schemas import EventType, utc_now_iso


# Global or per-run event emitters
_active_emitters: Dict[str, ExecutionEventEmitter] = {}


def get_emitter_for_run(run_id: str) -> ExecutionEventEmitter:
    if run_id not in _active_emitters:
        emitter = ExecutionEventEmitter(run_id=run_id)
        # Add persistence listener
        emitter.subscribe(
            lambda evt: save_execution_event(
                run_id=evt.run_id,
                event_id=evt.event_id,
                agent_name=evt.agent_name,
                node_name=evt.node_name,
                event_type=evt.event_type.value,
                status=evt.status,
                message=evt.message,
                duration_ms=evt.duration_ms,
            )
        )
        _active_emitters[run_id] = emitter
    return _active_emitters[run_id]


# -------------------------------------------------------------
# Node 1: Request Validation
# -------------------------------------------------------------
def validate_request_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    research_id = state.get("research_id") or str(uuid.uuid4())
    emitter = get_emitter_for_run(research_id)

    objective = (state.get("research_objective") or "").strip()
    errors = []

    if not objective:
        errors.append("Research objective cannot be empty.")
        emitter.emit(
            event_type=EventType.RESEARCH_FAILED,
            agent_name="System",
            node_name="validate_request",
            message="Research failed: Missing research objective.",
            status="failed",
        )
        return {
            "research_id": research_id,
            "research_status": "failed",
            "errors": errors,
        }

    duration_ms = int((time.time() - start_time) * 1000)
    emitter.emit(
        event_type=EventType.RESEARCH_STARTED,
        agent_name="System",
        node_name="validate_request",
        message=f"Research session initialized for objective: '{objective[:80]}...'",
        status="completed",
        duration_ms=duration_ms,
    )

    return {
        "research_id": research_id,
        "research_objective": objective,
        "industry": state.get("industry", "General Business"),
        "geography": state.get("geography", "Global"),
        "time_horizon": state.get("time_horizon", "Current (Real-time)"),
        "research_status": "planning",
        "iteration_count": 1,
        "evidence_registry": [],
        "errors": [],
    }


# -------------------------------------------------------------
# Node 2: Question Decomposition (Research Director)
# -------------------------------------------------------------
def decompose_questions_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    plan = create_research_plan(
        objective=state["research_objective"],
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        time_horizon=state.get("time_horizon", "Current (Real-time)"),
    )

    duration_ms = int((time.time() - start_time) * 1000)
    emitter.emit(
        event_type=EventType.RESEARCH_QUESTIONS_CREATED,
        agent_name="Research Director",
        node_name="decompose_questions",
        message=(
            f"Formulated {len(plan.get('research_questions', []))} research questions and "
            f"dispatched targeted queries to Market, Competitor, and Customer analysts."
        ),
        status="completed",
        duration_ms=duration_ms,
    )

    return {
        "research_plan": plan,
        "research_status": "investigating",
    }


# -------------------------------------------------------------
# Node 3: Market Intelligence Analyst
# -------------------------------------------------------------
def market_analyst_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    emitter.emit(
        event_type=EventType.SPECIALIST_STARTED,
        agent_name="Market Intelligence Analyst",
        node_name="market_analyst",
        message="Initiated search and source acquisition on market structure, trends, and growth.",
        status="running",
    )

    plan = state.get("research_plan", {})
    queries = plan.get("market_queries", [
        f"{state.get('industry', '')} market trends {state.get('geography', '')}"
    ])

    result = run_market_analyst(
        objective=state["research_objective"],
        queries=queries,
        research_questions=plan.get("research_questions", []),
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        research_id=run_id,
    )

    evidence = result.pop("evidence", [])
    duration_ms = int((time.time() - start_time) * 1000)

    emitter.emit(
        event_type=EventType.SOURCE_RETRIEVAL_COMPLETED,
        agent_name="Market Intelligence Analyst",
        node_name="market_analyst",
        message=f"Acquired {len(result.get('sources', []))} sources and extracted {len(evidence)} evidence records.",
        status="completed",
        entity_ids=[e["evidence_id"] for e in evidence],
        duration_ms=duration_ms,
    )

    return {
        "market_report": result,
        "evidence_registry": evidence,
    }


# -------------------------------------------------------------
# Node 4: Competitor Intelligence Analyst
# -------------------------------------------------------------
def competitor_analyst_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    emitter.emit(
        event_type=EventType.SPECIALIST_STARTED,
        agent_name="Competitor Intelligence Analyst",
        node_name="competitor_analyst",
        message="Initiated search on competitors, positioning, pricing, and capabilities.",
        status="running",
    )

    plan = state.get("research_plan", {})
    queries = plan.get("competitor_queries", [
        f"leading {state.get('industry', '')} competitors {state.get('geography', '')}"
    ])

    result = run_competitor_analyst(
        objective=state["research_objective"],
        queries=queries,
        research_questions=plan.get("research_questions", []),
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        research_id=run_id,
    )

    evidence = result.pop("evidence", [])
    duration_ms = int((time.time() - start_time) * 1000)

    emitter.emit(
        event_type=EventType.SOURCE_RETRIEVAL_COMPLETED,
        agent_name="Competitor Intelligence Analyst",
        node_name="competitor_analyst",
        message=f"Acquired {len(result.get('sources', []))} sources and extracted {len(evidence)} evidence records.",
        status="completed",
        entity_ids=[e["evidence_id"] for e in evidence],
        duration_ms=duration_ms,
    )

    return {
        "competitor_report": result,
        "evidence_registry": evidence,
    }


# -------------------------------------------------------------
# Node 5: Customer Intelligence Analyst
# -------------------------------------------------------------
def customer_analyst_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    emitter.emit(
        event_type=EventType.SPECIALIST_STARTED,
        agent_name="Customer Intelligence Analyst",
        node_name="customer_analyst",
        message="Initiated search on customer pain points, buying behavior, and unmet needs.",
        status="running",
    )

    plan = state.get("research_plan", {})
    queries = plan.get("customer_queries", [
        f"{state.get('industry', '')} customer pain points {state.get('geography', '')}"
    ])

    result = run_customer_analyst(
        objective=state["research_objective"],
        queries=queries,
        research_questions=plan.get("research_questions", []),
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        research_id=run_id,
    )

    evidence = result.pop("evidence", [])
    duration_ms = int((time.time() - start_time) * 1000)

    emitter.emit(
        event_type=EventType.SOURCE_RETRIEVAL_COMPLETED,
        agent_name="Customer Intelligence Analyst",
        node_name="customer_analyst",
        message=f"Acquired {len(result.get('sources', []))} sources and extracted {len(evidence)} evidence records.",
        status="completed",
        entity_ids=[e["evidence_id"] for e in evidence],
        duration_ms=duration_ms,
    )

    return {
        "customer_report": result,
        "evidence_registry": evidence,
    }


# -------------------------------------------------------------
# Node 6: Cross-Agent Synthesis & Verification
# -------------------------------------------------------------
def cross_agent_synthesis_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    # 1. Aggregate sources and quality assessments from all specialists
    specialist_reports = [
        state.get("market_report", {}),
        state.get("competitor_report", {}),
        state.get("customer_report", {}),
    ]

    all_sources = []
    source_qualities = {}
    all_claims = []
    all_gaps = []

    for rep in specialist_reports:
        if not rep:
            continue
        all_sources.extend(rep.get("sources", []))
        source_qualities.update(rep.get("source_qualities", {}))
        all_claims.extend(rep.get("claims", []))
        all_gaps.extend(rep.get("research_gaps", []))

    evidence_registry = state.get("evidence_registry", [])

    # 2. Duplicate Detection & Clustering
    evidence_groups = cluster_sources_and_evidence(
        sources=all_sources,
        evidence=evidence_registry,
    )
    if evidence_groups:
        emitter.emit(
            event_type=EventType.DUPLICATE_DETECTED,
            agent_name="Verification Engine",
            node_name="cross_agent_synthesis",
            message=f"Clustered sources into {len(evidence_groups)} unique canonical evidence groups.",
            status="completed",
            entity_ids=[g.group_id for g in evidence_groups],
        )

    # 3. Contradiction Detection
    contradictions = detect_contradictions(
        claims=all_claims,
        evidence=evidence_registry,
    )
    if contradictions:
        emitter.emit(
            event_type=EventType.CONTRADICTION_DETECTED,
            agent_name="Verification Engine",
            node_name="cross_agent_synthesis",
            message=f"Flagged {len(contradictions)} potential contradictory findings across agents.",
            status="completed",
            entity_ids=[c.contradiction_id for c in contradictions],
        )

    # 4. Claim-Level Verification
    emitter.emit(
        event_type=EventType.CLAIM_VERIFICATION_STARTED,
        agent_name="Verification Engine",
        node_name="cross_agent_synthesis",
        message=f"Beginning claim-level verification across {len(all_claims)} candidate claims.",
        status="running",
    )

    verifications = verify_claims_against_evidence(
        claims=all_claims,
        evidence=evidence_registry,
        sources=all_sources,
        source_qualities=source_qualities,
        contradictions=contradictions,
    )

    # 5. Citation Validation and Traceability
    validated_claims = validate_citations_and_traceability(
        claims=all_claims,
        evidence=evidence_registry,
    )

    verified_count = sum(1 for c in validated_claims if getattr(c, "verification_status", "") == "supported" or (isinstance(c, dict) and c.get("verification_status") == "supported"))

    duration_ms = int((time.time() - start_time) * 1000)
    emitter.emit(
        event_type=EventType.CLAIM_VERIFIED,
        agent_name="Verification Engine",
        node_name="cross_agent_synthesis",
        message=f"Verified {verified_count} of {len(validated_claims)} claims with direct evidence traceability.",
        status="completed",
        duration_ms=duration_ms,
    )

    return {
        "sources": all_sources,
        "source_qualities": source_qualities,
        "evidence_groups": evidence_groups,
        "claims": validated_claims,
        "verifications": verifications,
        "contradictions": contradictions,
        "research_gaps": all_gaps,
    }


# -------------------------------------------------------------
# Node 7: Research Director Executive Review & Report Generation
# -------------------------------------------------------------
def director_review_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    emitter.emit(
        event_type=EventType.DIRECTOR_REVIEW_STARTED,
        agent_name="Research Director",
        node_name="director_review",
        message="Synthesizing multi-agent intelligence, business opportunities, and strategic recommendations.",
        status="running",
    )

    specialist_reports = {
        "market": state.get("market_report", {}),
        "competitors": state.get("competitor_report", {}),
        "customers": state.get("customer_report", {}),
    }

    final_report = synthesize_executive_intelligence(
        research_id=run_id,
        objective=state["research_objective"],
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        specialist_reports=specialist_reports,
        sources=state.get("sources", []),
        evidence=state.get("evidence_registry", []),
        claims=state.get("claims", []),
        contradictions=state.get("contradictions", []),
        research_gaps=state.get("research_gaps", []),
    )

    duration_ms = int((time.time() - start_time) * 1000)
    emitter.emit(
        event_type=EventType.REPORT_GENERATED,
        agent_name="Research Director",
        node_name="director_review",
        message=(
            f"Executive Intelligence Report compiled. "
            f"Research Quality: {final_report.get('research_quality')} | "
            f"Verification: {final_report.get('verification_status')}"
        ),
        status="completed",
        duration_ms=duration_ms,
    )

    return {
        "final_report": final_report,
        "status_dimensions": {
            "execution_status": final_report.get("status", "completed"),
            "research_quality": final_report.get("research_quality", "moderate"),
            "verification_status": final_report.get("verification_status", "partially_verified"),
        },
        "research_status": final_report.get("status", "completed"),
    }


# -------------------------------------------------------------
# Node 8: Persistence
# -------------------------------------------------------------
def persist_results_node(state: MarketPulseState) -> Dict[str, Any]:
    start_time = time.time()
    run_id = state["research_id"]
    emitter = get_emitter_for_run(run_id)

    try:
        save_complete_research_run(state)
        duration_ms = int((time.time() - start_time) * 1000)
        emitter.emit(
            event_type=EventType.RESEARCH_COMPLETED,
            agent_name="Persistence Service",
            node_name="persist_results",
            message=f"All research runs, sources, evidence, claims, and artifacts safely stored in SQLite.",
            status="completed",
            duration_ms=duration_ms,
        )
    except Exception as exc:
        emitter.emit(
            event_type=EventType.RESEARCH_FAILED,
            agent_name="Persistence Service",
            node_name="persist_results",
            message=f"Database persistence warning: {exc}",
            status="failed",
        )

    return {
        "research_status": "completed",
    }
