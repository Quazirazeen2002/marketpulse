"""
REST API endpoints for MARKETPULSE Stage 2 — Strategic Intelligence & Autonomous Opportunity Discovery.
Mounts at `/api/strategic` to provide execution dispatch, progress tracking,
opportunity exploration, hypothesis tracking, risk assessment, and financial scenario simulations.
"""

import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.strategic import (
    StrategicResearchRequest,
    ScenarioInput,
    BusinessScenario,
)
from app.services.task_manager import task_manager
from app.database.repository import (
    get_research_run,
    get_strategic_analysis,
    list_strategic_analyses,
    get_strategic_opportunities,
    get_strategic_hypotheses,
    get_strategic_risks,
    get_strategic_events,
    get_stored_scenarios,
    get_opportunity_by_id,
    get_marketing_intelligence,
    get_commercial_intelligence,
    save_scenario_simulation,
    list_all_opportunities,
    list_all_hypotheses,
    list_all_risks,
)
from app.services.business_simulation import generate_scenario_suite, run_sensitivity_analysis

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/strategic", tags=["Strategic Intelligence"])


@router.post("/analyses", status_code=status.HTTP_202_ACCEPTED)
def start_strategic_analysis(payload: StrategicResearchRequest):
    """
    Dispatch an autonomous strategic intelligence and opportunity discovery workflow
    for a completed Stage 1 research run.
    Returns HTTP 202 immediately with strategic analysis ID.
    """
    if not payload.research_id or not payload.research_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="research_id is required."
        )

    # Verify Stage 1 research run exists
    run = get_research_run(payload.research_id)
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stage 1 research run '{payload.research_id}' was not found. Please complete Stage 1 first."
        )

    task_info = task_manager.submit_strategic_task(
        research_id=payload.research_id,
        strategic_objective=payload.strategic_objective or "",
        max_research_iterations=payload.max_research_iterations,
        max_followup_searches=payload.max_followup_searches,
        max_followup_tasks=payload.max_followup_tasks,
    )

    return task_info


@router.get("/analyses")
def list_analyses(
    research_id: Optional[str] = Query(None, description="Filter by Stage 1 research ID"),
    limit: int = Query(50, ge=1, le=100)
):
    """List historical strategic analyses."""
    return list_strategic_analyses(research_id=research_id, limit=limit)


@router.get("/analyses/{analysis_id}")
def get_analysis_metadata(analysis_id: str):
    """Retrieve metadata, plan, and high-level metrics for a strategic analysis."""
    analysis = get_strategic_analysis(analysis_id)
    if not analysis:
        # Check in memory if currently executing
        progress = task_manager.get_strategic_progress(analysis_id)
        if progress:
            return progress
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategic analysis '{analysis_id}' not found."
        )
    return analysis


@router.get("/analyses/{analysis_id}/progress")
def get_analysis_progress(analysis_id: str):
    """
    Poll live progress and real execution events for an active or completed strategic analysis.
    """
    progress = task_manager.get_strategic_progress(analysis_id)
    if not progress:
        analysis = get_strategic_analysis(analysis_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Strategic analysis '{analysis_id}' not found."
            )
        events = get_strategic_events(analysis_id)
        return {
            "analysis_id": analysis["id"],
            "research_id": analysis["research_id"],
            "execution_status": analysis["status"],
            "current_stage": "completed" if analysis["status"] == "completed" else analysis["status"],
            "elapsed_seconds": 0,
            "specialist_status": {
                s: "completed"
                for s in (
                    "Research Director",
                    "Marketing Intelligence Analyst",
                    "Commercial Intelligence Analyst",
                    "Opportunity Discovery Analyst",
                    "Risk & Industry Intelligence Analyst",
                )
            },
            "opportunities_count": analysis.get("total_opportunities", 0),
            "hypotheses_count": analysis.get("total_hypotheses", 0),
            "risks_count": analysis.get("total_risks", 0),
            "progress_events": events,
            "error": None,
        }
    return progress


@router.get("/analyses/{analysis_id}/report")
def get_analysis_report(analysis_id: str):
    """Retrieve the finalized 10-section strategic executive report."""
    analysis = get_strategic_analysis(analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Strategic analysis '{analysis_id}' not found."
        )
    final_report = analysis.get("final_report")
    if not final_report:
        # Check active memory
        progress = task_manager.strategic_tasks.get(analysis_id, {})
        report = progress.get("strategic_report")
        if report:
            return report
        return {
            "status": analysis.get("status"),
            "message": "Strategic executive report is being prepared by Research Director.",
        }
    return final_report


@router.get("/analyses/{analysis_id}/opportunities")
def get_analysis_opportunities(analysis_id: str):
    """Retrieve all discovered opportunities and deterministic scores for a strategic analysis."""
    opps = get_strategic_opportunities(analysis_id)
    return opps


@router.get("/analyses/{analysis_id}/hypotheses")
def get_analysis_hypotheses(analysis_id: str):
    """Retrieve all research hypotheses and investigation statuses for an analysis."""
    return get_strategic_hypotheses(analysis_id)


@router.get("/analyses/{analysis_id}/risks")
def get_analysis_risks(analysis_id: str):
    """Retrieve all risk assessments for an analysis."""
    return get_strategic_risks(analysis_id)


@router.get("/analyses/{analysis_id}/events")
def get_analysis_events(analysis_id: str):
    """Retrieve full chronological execution audit events for an analysis."""
    return get_strategic_events(analysis_id)


@router.get("/analyses/{analysis_id}/scenarios")
def get_analysis_scenarios(analysis_id: str):
    """Retrieve stored financial scenarios and simulations for an analysis."""
    return get_stored_scenarios(analysis_id)


@router.get("/analyses/{analysis_id}/marketing")
def get_analysis_marketing(analysis_id: str):
    """Retrieve brand, campaign, channel intelligence and marketing gaps."""
    marketing = get_marketing_intelligence(analysis_id)
    if not marketing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Marketing intelligence for analysis '{analysis_id}' not found."
        )
    return marketing


@router.get("/analyses/{analysis_id}/commercial")
def get_analysis_commercial(analysis_id: str):
    """Retrieve pricing structures, monetization models, delivery charges, and gaps."""
    commercial = get_commercial_intelligence(analysis_id)
    if not commercial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Commercial intelligence for analysis '{analysis_id}' not found."
        )
    return commercial


@router.get("/opportunities")
def list_opportunities_endpoint(
    analysis_id: Optional[str] = Query(None, description="Optional strategic analysis ID filter"),
    limit: int = Query(100, ge=1, le=200),
):
    """Retrieve all discovered opportunities, sorted by risk-adjusted score."""
    return list_all_opportunities(analysis_id=analysis_id, limit=limit)


@router.get("/hypotheses")
def list_hypotheses_endpoint(
    analysis_id: Optional[str] = Query(None, description="Optional strategic analysis ID filter"),
    limit: int = Query(100, ge=1, le=200),
):
    """Retrieve all research hypotheses across investigations."""
    return list_all_hypotheses(analysis_id=analysis_id, limit=limit)


@router.get("/risks")
def list_risks_endpoint(
    analysis_id: Optional[str] = Query(None, description="Optional strategic analysis ID filter"),
    limit: int = Query(100, ge=1, le=200),
):
    """Retrieve all risk assessments across investigations."""
    return list_all_risks(analysis_id=analysis_id, limit=limit)


@router.get("/opportunities/{opportunity_id}")
def get_opportunity_details(opportunity_id: str):
    """Retrieve complete investigation details, evidence links, and score breakdown for an opportunity."""
    opp = get_opportunity_by_id(opportunity_id)
    if not opp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Opportunity '{opportunity_id}' not found."
        )
    return opp


@router.post("/opportunities/{opportunity_id}/simulate")
def simulate_opportunity_business(
    opportunity_id: str,
    payload: ScenarioInput,
):
    """
    Run a deterministic financial scenario simulation for a discovered business opportunity.
    Computes Base, Best, and Worst case outcomes + 5D sensitivity analysis.
    Stores the scenario in SQLite.
    """
    opp = get_opportunity_by_id(opportunity_id)
    opp_name = opp.get("opportunity_name", f"Opportunity {opportunity_id}") if opp else f"Opportunity {opportunity_id}"
    analysis_id = opp.get("strategic_analysis_id", "") if opp else ""
    research_id = opp.get("research_id", "") if opp else ""

    # Generate deterministic financial scenario suite
    suite = generate_scenario_suite(payload)
    sensitivity = run_sensitivity_analysis(payload)

    # Save to SQLite if opportunity is associated with a recorded analysis
    if analysis_id:
        try:
            save_scenario_simulation(
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                opportunity_id=opportunity_id,
                scenario_suite={
                    "base_case": suite["base_case"].model_dump(),
                    "best_case": suite["best_case"].model_dump(),
                    "worst_case": suite["worst_case"].model_dump(),
                },
            )
        except Exception as exc:
            logger.warning("Failed to persist scenario simulation for opportunity %s: %s", opportunity_id, exc)

    return {
        "opportunity_id": opportunity_id,
        "opportunity_name": opp_name,
        "base_case": suite["base_case"].model_dump(),
        "best_case": suite["best_case"].model_dump(),
        "worst_case": suite["worst_case"].model_dump(),
        "sensitivity": [s.model_dump() for s in sensitivity],
        "simulation_notes": [
            "Deterministic financial calculation performed by MarketPulse Simulation Engine.",
            "Assumptions are user-editable; outputs reflect specified unit economics.",
        ],
    }
