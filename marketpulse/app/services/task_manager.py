"""
Background Task Manager for MARKETPULSE.
Manages asynchronous execution of LangGraph multi-agent research workflows
outside of HTTP request handlers using a bounded ThreadPoolExecutor.
Supports live progress polling, agent telemetry updates, and reconnection.
"""

import time
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional

from app.graph.builder import marketpulse_graph
from app.graph.nodes import get_emitter_for_run
from app.database.repository import (
    get_research_run,
    get_run_sources,
    get_run_evidence,
    get_run_claims,
    get_run_contradictions,
    get_run_events,
)
from app.schemas import EventType

logger = logging.getLogger(__name__)


class TaskManager:
    """
    In-process task manager executing research runs on worker threads.
    Maintains real-time execution progress, events, and metrics.
    """

    def __init__(self, max_workers: int = 3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="marketpulse_worker")
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.strategic_tasks: Dict[str, Dict[str, Any]] = {}

    def submit_research_task(
        self,
        objective: str,
        industry: str = "General Business",
        geography: str = "Global",
        time_horizon: str = "Current (Real-time)",
        research_depth: str = "deep",
        additional_instructions: str = "",
    ) -> Dict[str, Any]:
        """
        Create a new research run, initialize task state, and dispatch to worker.
        Returns immediately with research metadata.
        """
        research_id = str(uuid.uuid4())

        task_record = {
            "research_id": research_id,
            "objective": objective.strip(),
            "industry": industry,
            "geography": geography,
            "time_horizon": time_horizon,
            "research_depth": research_depth,
            "additional_instructions": additional_instructions,
            "execution_status": "pending",
            "current_stage": "request_validation",
            "start_time": time.time(),
            "elapsed_seconds": 0,
            "progress_events": [],
            "agent_status": {
                "Research Director": "planning",
                "Market Intelligence Analyst": "waiting",
                "Competitor Intelligence Analyst": "waiting",
                "Customer Intelligence Analyst": "waiting",
            },
            "source_count": 0,
            "full_text_sources": 0,
            "evidence_count": 0,
            "verified_claim_count": 0,
            "contradictions_count": 0,
            "error": None,
            "completed_at": None,
            "final_report": None,
        }

        self.tasks[research_id] = task_record

        # Submit to background executor
        self.executor.submit(self._run_research_workflow, research_id)

        return {
            "research_id": research_id,
            "execution_status": "pending",
            "message": "Research task accepted and queued for execution.",
        }

    def _run_research_workflow(self, research_id: str) -> None:
        """Worker thread entrypoint running the LangGraph state machine."""
        task = self.tasks.get(research_id)
        if not task:
            return

        task["execution_status"] = "running"
        start_time = time.time()

        emitter = get_emitter_for_run(research_id)

        def _on_event(evt):
            task["elapsed_seconds"] = int(time.time() - start_time)
            task["progress_events"].append({
                "event_id": evt.event_id,
                "timestamp": evt.timestamp,
                "agent_name": evt.agent_name,
                "node_name": evt.node_name,
                "event_type": evt.event_type.value,
                "status": evt.status,
                "message": evt.message,
                "duration_ms": evt.duration_ms,
            })

            # Update specific agent status
            if evt.agent_name in task["agent_status"]:
                task["agent_status"][evt.agent_name] = evt.status

            if evt.event_type == EventType.RESEARCH_QUESTIONS_CREATED:
                task["current_stage"] = "research_planning"
            elif evt.event_type == EventType.SPECIALIST_STARTED:
                task["current_stage"] = "parallel_specialist_research"
            elif evt.event_type == EventType.SOURCE_RETRIEVAL_COMPLETED:
                task["source_count"] += len(evt.entity_ids or [])
            elif evt.event_type == EventType.CLAIM_VERIFICATION_STARTED:
                task["current_stage"] = "claim_verification"
            elif evt.event_type == EventType.CONTRADICTION_DETECTED:
                task["contradictions_count"] += len(evt.entity_ids or [])
            elif evt.event_type == EventType.CLAIM_VERIFIED:
                task["current_stage"] = "claim_verification"
            elif evt.event_type == EventType.DIRECTOR_REVIEW_STARTED:
                task["current_stage"] = "executive_synthesis"
            elif evt.event_type == EventType.REPORT_GENERATED:
                task["current_stage"] = "report_generated"
            elif evt.event_type == EventType.RESEARCH_COMPLETED:
                task["current_stage"] = "completed"

        emitter.subscribe(_on_event)

        initial_state = {
            "research_id": research_id,
            "research_objective": task["objective"],
            "industry": task["industry"],
            "geography": task["geography"],
            "time_horizon": task["time_horizon"],
            "research_plan": {},
            "market_report": {},
            "competitor_report": {},
            "customer_report": {},
            "sources": [],
            "source_qualities": {},
            "evidence_registry": [],
            "evidence_groups": [],
            "claims": [],
            "verifications": [],
            "contradictions": [],
            "research_gaps": [],
            "status_dimensions": {},
            "final_report": {},
            "research_status": "planning",
            "errors": [],
        }

        try:
            for event in marketpulse_graph.stream(initial_state, config={"recursion_limit": 25}):
                task["elapsed_seconds"] = int(time.time() - start_time)
                for node_name, output in event.items():
                    if node_name == "validate_request":
                        task["current_stage"] = "request_validation"
                    elif node_name == "decompose_questions":
                        task["current_stage"] = "research_planning"
                    elif node_name in ("market_analyst", "competitor_analyst", "customer_analyst"):
                        task["current_stage"] = "parallel_specialist_research"
                        ev_list = output.get("evidence_registry", [])
                        task["evidence_count"] += len(ev_list)
                    elif node_name == "cross_agent_synthesis":
                        task["current_stage"] = "claim_verification"
                        claims = output.get("claims", [])
                        task["verified_claim_count"] = sum(
                            1 for c in claims
                            if getattr(c, "verification_status", "") == "supported"
                            or (isinstance(c, dict) and c.get("verification_status") == "supported")
                        )
                        task["contradictions_count"] = len(output.get("contradictions", []))
                        task["source_count"] = len(output.get("sources", []))
                    elif node_name == "director_review":
                        task["current_stage"] = "executive_synthesis"
                        task["final_report"] = output.get("final_report")
                    elif node_name == "persist_results":
                        task["current_stage"] = "completed"

            task["execution_status"] = "completed"
            task["completed_at"] = time.time()
            task["elapsed_seconds"] = int(time.time() - start_time)

        except Exception as exc:
            logger.exception("Error executing research workflow: %s", exc)
            task["execution_status"] = "failed"
            task["error"] = str(exc)
            task["current_stage"] = "failed"
            task["completed_at"] = time.time()
            task["elapsed_seconds"] = int(time.time() - start_time)

    def get_progress(self, research_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve live progress of an active task or restore from database."""
        if research_id in self.tasks:
            t = self.tasks[research_id]
            if t["execution_status"] == "running":
                t["elapsed_seconds"] = int(time.time() - t["start_time"])
            return t

        # Reconnect / fetch from SQLite if not currently in memory
        run = get_research_run(research_id)
        if run:
            sources = get_run_sources(research_id)
            evidence = get_run_evidence(research_id)
            claims = get_run_claims(research_id)
            contradictions = get_run_contradictions(research_id)
            events = get_run_events(research_id)

            return {
                "research_id": run["id"],
                "objective": run["objective"],
                "industry": run["industry"],
                "geography": run["geography"],
                "time_horizon": run["time_horizon"],
                "execution_status": run["status"],
                "current_stage": "completed" if run["status"] == "completed" else run["status"],
                "elapsed_seconds": 0,
                "progress_events": events,
                "agent_status": {
                    "Research Director": "completed",
                    "Market Intelligence Analyst": "completed",
                    "Competitor Intelligence Analyst": "completed",
                    "Customer Intelligence Analyst": "completed",
                },
                "source_count": len(sources),
                "full_text_sources": sum(1 for s in sources if s.get("extraction_status") == "retrieved_full_text"),
                "evidence_count": len(evidence),
                "verified_claim_count": sum(1 for c in claims if c.get("verification_status") == "supported"),
                "contradictions_count": len(contradictions),
                "final_report": run.get("final_report"),
                "error": None,
            }

        return None

    def get_active_count(self) -> int:
        """Count currently running tasks."""
        return sum(1 for t in self.tasks.values() if t.get("execution_status") == "running")

    def list_active_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks active in memory."""
        return [
            {
                "research_id": t["research_id"],
                "objective": t["objective"],
                "industry": t["industry"],
                "geography": t["geography"],
                "execution_status": t["execution_status"],
                "current_stage": t["current_stage"],
                "elapsed_seconds": t["elapsed_seconds"],
            }
            for t in self.tasks.values()
        ]


    def submit_strategic_task(
        self,
        research_id: str,
        strategic_objective: Optional[str] = None,
        max_research_iterations: int = 3,
        max_followup_searches: int = 4,
        max_followup_tasks: int = 8,
    ) -> Dict[str, Any]:
        """Submit an autonomous strategic intelligence and opportunity discovery task."""
        analysis_id = str(uuid.uuid4())
        task_record = {
            "analysis_id": analysis_id,
            "research_id": research_id,
            "strategic_objective": strategic_objective or "",
            "max_research_iterations": max_research_iterations,
            "max_followup_searches": max_followup_searches,
            "max_followup_tasks": max_followup_tasks,
            "execution_status": "pending",
            "current_stage": "load_stage1_research",
            "start_time": time.time(),
            "elapsed_seconds": 0,
            "progress_events": [],
            "specialist_status": {
                "Research Director": "planning",
                "Marketing Intelligence Analyst": "waiting",
                "Commercial Intelligence Analyst": "waiting",
                "Opportunity Discovery Analyst": "waiting",
                "Risk & Industry Intelligence Analyst": "waiting",
            },
            "opportunities_count": 0,
            "hypotheses_count": 0,
            "risks_count": 0,
            "error": None,
            "completed_at": None,
            "strategic_report": None,
        }
        self.strategic_tasks[analysis_id] = task_record
        self.executor.submit(self._run_strategic_workflow, analysis_id)
        return {
            "analysis_id": analysis_id,
            "research_id": research_id,
            "execution_status": "pending",
            "message": "Strategic intelligence workflow accepted and queued.",
        }

    def _run_strategic_workflow(self, analysis_id: str) -> None:
        """Worker thread executing the Stage 2 Strategic LangGraph StateMachine."""
        task = self.strategic_tasks.get(analysis_id)
        if not task:
            return

        task["execution_status"] = "running"
        start_time = time.time()
        research_id = task["research_id"]

        initial_state = {
            "strategic_analysis_id": analysis_id,
            "research_id": research_id,
            "strategic_objective": task["strategic_objective"],
            "research_iterations": 1,
            "search_budget": {
                "max_iterations": task["max_research_iterations"],
                "max_searches": task["max_followup_searches"],
                "max_tasks": task["max_followup_tasks"],
            },
            "execution_status": "running",
            "errors": [],
        }

        try:
            from app.graph.strategic_workflow import strategic_graph
            for event in strategic_graph.stream(initial_state, config={"recursion_limit": 25}):
                task["elapsed_seconds"] = int(time.time() - start_time)
                for node_name, output in event.items():
                    if node_name == "load_stage1_research":
                        task["current_stage"] = "stage1_loaded"
                    elif node_name == "strategic_planning":
                        task["current_stage"] = "strategic_planning"
                        task["specialist_status"]["Research Director"] = "running"
                    elif node_name == "parallel_specialists":
                        task["current_stage"] = "parallel_specialists_complete"
                        for s in task["specialist_status"]:
                            task["specialist_status"][s] = "completed"
                        task["opportunities_count"] = len(output.get("opportunities", []))
                    elif node_name == "strategic_synthesis":
                        task["current_stage"] = "synthesis_and_gaps"
                        task["hypotheses_count"] = len(output.get("hypotheses", []))
                    elif node_name == "followup_investigation":
                        task["current_stage"] = "followup_investigation"
                    elif node_name == "opportunity_scoring":
                        task["current_stage"] = "opportunity_scoring"
                    elif node_name == "scenario_simulation":
                        task["current_stage"] = "scenario_simulation"
                    elif node_name == "strategic_executive_report":
                        task["current_stage"] = "report_generated"
                        task["strategic_report"] = output.get("strategic_report")
                    elif node_name == "persist_strategic_analysis":
                        task["current_stage"] = "completed"

            task["execution_status"] = "completed"
            task["completed_at"] = time.time()
            task["elapsed_seconds"] = int(time.time() - start_time)
        except Exception as exc:
            logger.exception("Error executing strategic workflow %s: %s", analysis_id, exc)
            task["execution_status"] = "failed"
            task["error"] = str(exc)
            task["current_stage"] = "failed"
            task["completed_at"] = time.time()
            task["elapsed_seconds"] = int(time.time() - start_time)

    def get_strategic_progress(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve live execution progress and metrics for a strategic analysis."""
        if analysis_id in self.strategic_tasks:
            t = self.strategic_tasks[analysis_id]
            from app.database.repository import get_strategic_events
            persisted_events = get_strategic_events(analysis_id)
            return {
                "analysis_id": t["analysis_id"],
                "research_id": t["research_id"],
                "execution_status": t["execution_status"],
                "current_stage": t["current_stage"],
                "elapsed_seconds": t["elapsed_seconds"],
                "specialist_status": t["specialist_status"],
                "opportunities_count": t["opportunities_count"],
                "hypotheses_count": t["hypotheses_count"],
                "risks_count": t["risks_count"],
                "progress_events": persisted_events or t["progress_events"],
                "error": t["error"],
            }
        from app.database.repository import get_strategic_analysis, get_strategic_events
        saved = get_strategic_analysis(analysis_id)
        if saved:
            events = get_strategic_events(analysis_id)
            return {
                "analysis_id": saved["id"],
                "research_id": saved["research_id"],
                "execution_status": saved["status"],
                "current_stage": "completed" if saved["status"] == "completed" else saved["status"],
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
                "opportunities_count": saved.get("total_opportunities", 0),
                "hypotheses_count": saved.get("total_hypotheses", 0),
                "risks_count": saved.get("total_risks", 0),
                "progress_events": events,
                "error": None,
            }
        return None

    def shutdown(self, wait: bool = False):
        """Shut down background thread pool executor."""
        logger.info("Shutting down TaskManager worker pool...")
        self.executor.shutdown(wait=wait, cancel_futures=True)


# Global singleton instance
task_manager = TaskManager(max_workers=3)

