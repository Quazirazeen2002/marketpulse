"""
REST API routers for MARKETPULSE Stage 1.
Provides research submission (HTTP 202), live progress polling,
report retrieval, exports, system health, and history.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field

from app.services.task_manager import task_manager
from app.database.repository import (
    list_research_runs,
    get_research_run,
    get_run_sources,
    get_run_evidence,
    get_run_claims,
    get_run_contradictions,
    get_run_events,
    compare_runs,
    get_overview_metrics,
    list_all_sources,
    list_all_evidence,
    list_all_claims,
)
from app.services.export.exporter import (
    export_markdown_report,
    export_json_report,
    export_evidence_csv,
    export_printable_html,
)
from app.models.gateway import (
    get_research_model,
    get_director_model,
    get_specialist_model,
    director_model_available,
    specialist_model_available,
)
from app.database.db import engine
from app.config import settings

router = APIRouter(prefix="/api", tags=["API"])


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------

class SubmitResearchRequest(BaseModel):
    objective: str = Field(..., min_length=5, description="Primary research objective")
    industry: str = Field("General Business", description="Target industry")
    geography: str = Field("Global", description="Target geography or market")
    time_horizon: str = Field("Current (Real-time)", description="Temporal research horizon")
    research_depth: str = Field("deep", description="Investigation depth: standard, deep, comprehensive")
    additional_instructions: Optional[str] = Field("", description="Optional custom constraints")


class CompareRunsRequest(BaseModel):
    run_id_a: str
    run_id_b: str


# -------------------------------------------------------------
# Research Endpoints
# -------------------------------------------------------------

@router.post("/research", status_code=status.HTTP_202_ACCEPTED)
def start_research(payload: SubmitResearchRequest):
    """
    Dispatch a deep research run in the background.
    Returns HTTP 202 immediately with research run ID.
    """
    if not payload.objective or not payload.objective.strip():
        raise HTTPException(status_code=400, detail="Research objective cannot be empty.")

    task_info = task_manager.submit_research_task(
        objective=payload.objective,
        industry=payload.industry,
        geography=payload.geography,
        time_horizon=payload.time_horizon,
        research_depth=payload.research_depth,
        additional_instructions=payload.additional_instructions or "",
    )

    return task_info


@router.get("/research/{research_id}/progress")
def get_research_progress(research_id: str):
    """
    Poll live execution progress for an active or completed research run.
    """
    progress = task_manager.get_progress(research_id)
    if not progress:
        raise HTTPException(status_code=404, detail=f"Research run '{research_id}' not found.")

    return progress


@router.get("/research/{research_id}/events/stream")
async def stream_research_events(research_id: str):
    """
    Server-Sent Events (SSE) stream for live research progress.
    Streams execution events, telemetry counters, and completion events in real time.
    Supports client reconnection and last-event tracking.
    """
    async def event_generator():
        last_event_idx = 0
        loop_count = 0
        while True:
            progress = task_manager.get_progress(research_id)
            if not progress:
                err_data = json.dumps({"type": "error", "message": f"Research run '{research_id}' not found."})
                yield f"data: {err_data}\n\n"
                break

            events = progress.get("progress_events", [])
            # Stream any newly appended events
            while last_event_idx < len(events):
                evt = events[last_event_idx]
                payload = {
                    "type": "event",
                    "event": evt,
                    "execution_status": progress.get("execution_status"),
                    "current_stage": progress.get("current_stage"),
                    "elapsed_seconds": progress.get("elapsed_seconds", 0),
                    "source_count": progress.get("source_count", 0),
                    "evidence_count": progress.get("evidence_count", 0),
                    "verified_claims_count": progress.get("verified_claims_count", 0),
                    "contradictions_count": progress.get("contradictions_count", 0),
                    "agent_status": progress.get("agent_status", {}),
                }
                yield f"data: {json.dumps(payload)}\n\n"
                last_event_idx += 1

            status = progress.get("execution_status")
            if status in ("completed", "failed"):
                # Send terminal status event with final report if available
                final_payload = {
                    "type": "status",
                    "execution_status": status,
                    "current_stage": progress.get("current_stage"),
                    "elapsed_seconds": progress.get("elapsed_seconds", 0),
                    "source_count": progress.get("source_count", 0),
                    "evidence_count": progress.get("evidence_count", 0),
                    "verified_claims_count": progress.get("verified_claims_count", 0),
                    "contradictions_count": progress.get("contradictions_count", 0),
                    "agent_status": progress.get("agent_status", {}),
                    "final_report": progress.get("final_report"),
                    "error": progress.get("error"),
                }
                yield f"data: {json.dumps(final_payload)}\n\n"
                break

            loop_count += 1
            if loop_count % 5 == 0:
                yield ": keepalive\n\n"

            await asyncio.sleep(1.0)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/research/{research_id}")
def get_research_details(research_id: str):
    """
    Get full metadata, quality dimensions, and status of a research run.
    """
    run = get_research_run(research_id)
    if not run:
        # Check active in-memory tasks
        progress = task_manager.get_progress(research_id)
        if progress:
            return progress
        raise HTTPException(status_code=404, detail=f"Research run '{research_id}' not found.")

    sources = get_run_sources(research_id)
    claims = get_run_claims(research_id)
    contradictions = get_run_contradictions(research_id)

    return {
        "metadata": run,
        "source_count": len(sources),
        "claim_count": len(claims),
        "contradictions_count": len(contradictions),
    }


@router.get("/research/{research_id}/report")
def get_research_report(research_id: str):
    """
    Retrieve completed executive research report.
    """
    run = get_research_run(research_id)
    if not run:
        progress = task_manager.get_progress(research_id)
        if progress and progress["execution_status"] == "running":
            return Response(
                content='{"status": "running", "message": "Research investigation still in progress."}',
                status_code=status.HTTP_202_ACCEPTED,
                media_type="application/json",
            )
        raise HTTPException(status_code=404, detail="Research report not found.")

    report = run.get("final_report", {})
    if not report:
        raise HTTPException(status_code=404, detail="Executive report not yet compiled.")

    return report


@router.get("/research/{research_id}/export/{export_format}")
def export_research_report(research_id: str, export_format: str):
    """
    Export research report as Markdown, JSON, CSV, or HTML.
    """
    run = get_research_run(research_id)
    if not run:
        raise HTTPException(status_code=404, detail="Research run not found.")

    report = run.get("final_report", {})
    fmt = export_format.lower()

    if fmt == "markdown" or fmt == "md":
        content = export_markdown_report(report)
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=marketpulse_{research_id[:8]}.md"},
        )
    elif fmt == "json":
        content = export_json_report(report)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=marketpulse_{research_id[:8]}.json"},
        )
    elif fmt == "csv":
        evidence_list = get_run_evidence(research_id)
        content = export_evidence_csv(evidence_list)
        return Response(
            content=content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=marketpulse_evidence_{research_id[:8]}.csv"},
        )
    elif fmt == "html":
        content = export_printable_html(report)
        return Response(
            content=content,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename=marketpulse_{research_id[:8]}.html"},
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {export_format}")


@router.get("/research/{research_id}/sources")
def get_sources_endpoint(research_id: str):
    """Retrieve all acquired source documents for a research run."""
    return get_run_sources(research_id)


@router.get("/research/{research_id}/evidence")
def get_evidence_endpoint(research_id: str):
    """Retrieve all atomic evidence records for a research run."""
    return get_run_evidence(research_id)


@router.get("/research/{research_id}/claims")
def get_claims_endpoint(research_id: str):
    """Retrieve all claims and contradictions for a research run."""
    claims = get_run_claims(research_id)
    contradictions = get_run_contradictions(research_id)
    return {"claims": claims, "contradictions": contradictions}


@router.get("/research")
def list_research_history(limit: int = Query(50, ge=1, le=200)):
    """Retrieve paginated historical research runs."""
    return list_research_runs(limit=limit)


@router.post("/research/compare")
def compare_runs_endpoint(payload: CompareRunsRequest):
    """Compare two research runs across sources, claims, and deltas."""
    result = compare_runs(payload.run_id_a, payload.run_id_b)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/stats/overview")
def get_stats_overview():
    """Retrieve platform overview statistics and KPI metrics."""
    metrics = get_overview_metrics()
    metrics["active_investigations"] = task_manager.get_active_count()
    return metrics


@router.get("/sources")
def list_sources(research_id: Optional[str] = Query(None), limit: int = Query(100, ge=1, le=200)):
    """Retrieve sources across all research runs or filtered by research_id."""
    return list_all_sources(research_id=research_id, limit=limit)


@router.get("/evidence")
def list_evidence(research_id: Optional[str] = Query(None), limit: int = Query(100, ge=1, le=200)):
    """Retrieve atomic evidence records across all runs or filtered by research_id."""
    return list_all_evidence(research_id=research_id, limit=limit)


@router.get("/claims")
def list_claims(research_id: Optional[str] = Query(None), limit: int = Query(100, ge=1, le=200)):
    """Retrieve claims across all runs or filtered by research_id."""
    return list_all_claims(research_id=research_id, limit=limit)


# -------------------------------------------------------------
# Health & Telemetry Endpoints
# -------------------------------------------------------------

@router.get("/health")
def get_service_health():
    """Service health status and active worker count."""
    active_count = task_manager.get_active_count()
    return {
        "status": "healthy",
        "service": "MARKETPULSE",
        "version": "1.0.0",
        "architecture": "FastAPI + Jinja2 + LangGraph",
        "active_background_tasks": active_count,
    }


@router.get("/health/meta")
def check_meta_health():
    """Verify Meta AI reasoning models availability without exposing keys."""
    director_avail = director_model_available()
    specialist_avail = specialist_model_available()
    connected = director_avail or specialist_avail

    if not connected:
        return {
            "status": "unconfigured",
            "connected": False,
            "director_model": settings.META_MUSE_WONDER_MODEL,
            "specialist_model": settings.META_SPARK_MODEL,
            "message": "META_API_KEY is not set or gateway is offline. Running in deterministic heuristic mode.",
        }

    return {
        "status": "operational",
        "connected": True,
        "director_model": settings.META_MUSE_WONDER_MODEL,
        "specialist_model": settings.META_SPARK_MODEL,
        "model": f"{settings.META_MUSE_WONDER_MODEL} (Director) / {settings.META_SPARK_MODEL} (Specialists)",
        "provider": "Meta AI",
    }


@router.get("/health/tavily")
def check_tavily_health():
    """Verify Tavily Search API configuration and diagnostics without exposing credentials."""
    from app.services.web_search import tavily_search_client, search_cache, budget_manager
    total_cache_reqs = search_cache.hits + search_cache.misses
    hit_rate = round(search_cache.hits / total_cache_reqs * 100, 1) if total_cache_reqs > 0 else 0.0

    return {
        "status": "operational" if tavily_search_client.is_connected() else "unconfigured",
        "provider": "Tavily Search API",
        "connected": tavily_search_client.is_connected(),
        "search_depth": settings.TAVILY_SEARCH_DEPTH,
        "search_budget": settings.MAX_SEARCHES_PER_RESEARCH,
        "results_per_query": settings.TAVILY_MAX_RESULTS,
        "cache_enabled": settings.SEARCH_CACHE_ENABLED,
        "cache_ttl_hours": settings.SEARCH_CACHE_TTL_HOURS,
        "telemetry": {
            "search_requests": tavily_search_client.search_requests,
            "failed_requests": tavily_search_client.failed_requests,
            "total_results": tavily_search_client.total_results_returned,
            "cache_hits": search_cache.hits,
            "cache_misses": search_cache.misses,
            "cache_hit_rate": f"{hit_rate}%",
        },
    }



@router.get("/health/database")
def check_database_health():
    """Verify SQLite database connectivity and run counts."""
    try:
        from sqlmodel import Session, select, func
        from app.database.models import ResearchRun, EvidenceRecord

        with Session(engine) as session:
            run_count = session.exec(select(func.count(ResearchRun.id))).one()
            ev_count = session.exec(select(func.count(EvidenceRecord.id))).one()

        return {
            "status": "operational",
            "connected": True,
            "dialect": "sqlite",
            "total_research_runs": run_count,
            "total_evidence_records": ev_count,
        }
    except Exception as exc:
        return {
            "status": "degraded",
            "connected": False,
            "error": str(exc),
        }


@router.get("/agents")
def get_agent_directory(
    all: bool = Query(False, description="Include all 8 agents (Director + 7 Specialists)"),
    include_strategic: bool = Query(False, description="Alias for all")
):
    """Directory of available specialist agents and Director."""
    stage1_agents = [
        {
            "id": "director",
            "name": "Research Director",
            "role": "Chief Intelligence Synthesizer",
            "model": settings.META_MUSE_WONDER_MODEL,
            "responsibilities": [
                "Decompose objectives into searchable research questions",
                "Cross-examine specialist intelligence and detect contradictions",
                "Compute independent research quality and verification dimensions",
                "Synthesize executive reports with traceable citations",
            ],
            "status": "ready",
        },
        {
            "id": "market_analyst",
            "name": "Market Intelligence Analyst",
            "role": "Macro & Industry Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Investigate market structure, segmentation, and dynamics",
                "Verify market size and CAGR from authoritative sources",
                "Track regulatory shifts and emerging business models",
            ],
            "status": "ready",
        },
        {
            "id": "competitor_analyst",
            "name": "Competitor Intelligence Analyst",
            "role": "Competitive Strategy Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Identify direct and indirect competitors",
                "Benchmark positioning, pricing, and distribution models",
                "Identify competitor vulnerabilities and differentiation gaps",
            ],
            "status": "ready",
        },
        {
            "id": "customer_analyst",
            "name": "Customer Intelligence Analyst",
            "role": "Consumer & Demand Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Identify customer personas and purchase motivations",
                "Analyze customer complaints and friction points",
                "Uncover unmet customer needs and underserved niches",
            ],
            "status": "ready",
        },
    ]

    if not (all or include_strategic):
        return stage1_agents

    stage2_agents = [
        {
            "id": "marketing_analyst",
            "name": "Marketing Intelligence Analyst",
            "role": "Go-to-Market & Channel Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Analyze brand messaging, positioning, and marketing campaigns",
                "Detect high-ROI organic and paid customer acquisition channels",
                "Surface unexploited customer acquisition opportunities",
            ],
            "status": "ready",
        },
        {
            "id": "commercial_analyst",
            "name": "Commercial Intelligence Analyst",
            "role": "Pricing & Monetization Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Map competitor pricing tiers, fee structures, and margin models",
                "Identify hidden commercial friction and delivery cost gaps",
                "Model revenue streams and commercialization options",
            ],
            "status": "ready",
        },
        {
            "id": "opportunity_analyst",
            "name": "Opportunity Discovery Analyst",
            "role": "Autonomous Synthesis & Hypothesis Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Generate testable opportunity hypotheses from cross-domain signals",
                "Trigger autonomous follow-up web research queries",
                "Compute deterministic risk-adjusted opportunity scores",
            ],
            "status": "ready",
        },
        {
            "id": "risk_analyst",
            "name": "Risk & Industry Intelligence Analyst",
            "role": "Systemic Risk & Defense Specialist",
            "model": settings.META_SPARK_MODEL,
            "responsibilities": [
                "Assess regulatory, competitive, supply-chain, and execution risks",
                "Map 5x5 likelihood vs impact risk severity matrix",
                "Formulate actionable mitigation plans and compute residual risks",
            ],
            "status": "ready",
        },
    ]

    return stage1_agents + stage2_agents

