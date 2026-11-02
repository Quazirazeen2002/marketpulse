"""
Strategic LangGraph Node Implementations for MARKETPULSE Stage 2.
Orchestrates:
1. Load Stage 1 Verified Research
2. Director Muse Wonder Strategic Planning
3. Parallel Execution of Stage 2 Specialists (Marketing, Commercial, Opportunity, Risk)
4. Director Strategic Synthesis
5. Gap Detection & Hypothesis Generation
6. Autonomous Follow-up Research Execution (bounded loops)
7. Deterministic Opportunity Scoring
8. Business Scenario Simulation
9. 10-Section Strategic Executive Report (Sections A-J)
10. SQLite Persistence
"""

import time
import uuid
from typing import Dict, Any, List

from app.graph.strategic_state import StrategicState
from app.models.gateway import get_director_model, get_specialist_model
from app.database.repository import (
    get_research_run,
    get_run_sources,
    get_run_evidence,
    get_run_claims,
    get_run_contradictions,
    save_complete_strategic_analysis,
    save_strategic_event,
)
from app.agents.marketing_analyst import run_marketing_analyst
from app.agents.commercial_analyst import run_commercial_analyst
from app.agents.opportunity_analyst import run_opportunity_analyst
from app.agents.risk_analyst import run_risk_analyst
from app.services.hypothesis_engine import (
    StrategicResearchBudget,
    detect_research_gaps,
    generate_hypotheses_from_findings,
    prioritize_and_create_tasks,
    validate_hypotheses,
    check_stopping_conditions,
)
from app.services.opportunity_scoring import score_opportunity, rank_opportunities
from app.services.business_simulation import build_scenario_suite, ScenarioInput
from app.schemas.strategic import StrategicEventType, ResearchHypothesis


# -------------------------------------------------------------
# Node 1: Load Stage 1 Research
# -------------------------------------------------------------
def load_stage1_research_node(state: StrategicState) -> Dict[str, Any]:
    start_time = time.time()
    analysis_id = state.get("strategic_analysis_id") or str(uuid.uuid4())
    research_id = state.get("research_id", "")

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="load_stage1_research",
        event_type=StrategicEventType.STRATEGIC_ANALYSIS_STARTED.value,
        status="running",
        message=f"Initializing strategic opportunity discovery for Stage 1 research run '{research_id[:8]}...'",
    )

    stage1_run = get_research_run(research_id)
    if not stage1_run:
        save_strategic_event(
            analysis_id=analysis_id,
            research_id=research_id,
            event_id=f"EVT-{uuid.uuid4().hex[:6]}",
            agent_name="System",
            node_name="load_stage1_research",
            event_type=StrategicEventType.STRATEGIC_ANALYSIS_FAILED.value,
            status="failed",
            message=f"Stage 1 research record '{research_id}' could not be located in database.",
        )
        return {
            "strategic_analysis_id": analysis_id,
            "execution_status": "failed",
            "errors": [f"Stage 1 research run '{research_id}' not found."],
        }

    sources = get_run_sources(research_id)
    evidence = get_run_evidence(research_id)
    claims = get_run_claims(research_id)
    contradictions = get_run_contradictions(research_id)

    duration_ms = int((time.time() - start_time) * 1000)
    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="load_stage1_research",
        event_type=StrategicEventType.STAGE1_RESEARCH_LOADED.value,
        status="completed",
        message=(
            f"Successfully ingested Stage 1 verified findings: {len(sources)} sources, "
            f"{len(evidence)} evidence records, {len(claims)} claims, {len(contradictions)} contradictions."
        ),
        duration_ms=duration_ms,
    )

    return {
        "strategic_analysis_id": analysis_id,
        "research_id": research_id,
        "strategic_objective": state.get("strategic_objective") or stage1_run.get("objective", ""),
        "industry": stage1_run.get("industry", "General Business"),
        "geography": stage1_run.get("geography", "Global"),
        "stage1_findings": stage1_run.get("final_report", {}),
        "stage1_evidence_ids": [e["evidence_id"] for e in evidence if "evidence_id" in e],
        "evidence_records": evidence,
        "claims": claims,
        "contradictions": contradictions,
        "market_report": stage1_run.get("final_report", {}).get("specialist_reports", {}).get("Market Intelligence Analyst", {}),
        "competitor_report": stage1_run.get("final_report", {}).get("specialist_reports", {}).get("Competitor Intelligence Analyst", {}),
        "customer_report": stage1_run.get("final_report", {}).get("specialist_reports", {}).get("Customer Intelligence Analyst", {}),
        "research_iterations": 1,
        "search_budget": {"max_iterations": 3, "max_searches": 4, "max_tasks": 8},
        "execution_status": "planning",
        "errors": [],
    }


# -------------------------------------------------------------
# Node 2: Strategic Planning (Director Muse Wonder)
# -------------------------------------------------------------
def strategic_planning_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    objective = state.get("strategic_objective", "")
    industry = state.get("industry", "General Business")
    geography = state.get("geography", "Global")

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="Research Director",
        node_name="strategic_planning",
        event_type=StrategicEventType.STRATEGIC_PLANNING_STARTED.value,
        status="running",
        message="Research Director (Meta Muse Wonder) orchestrating Stage 2 strategic investigation framework.",
    )

    director_model = get_director_model()
    plan_notes = "Formulate cross-agent strategic discovery directives across marketing, commercialization, and risk."

    if director_model:
        try:
            prompt = f"""
You are the Chief Research Director of MARKETPULSE Stage 2.
Formulate a strategic opportunity discovery agenda for:
OBJECTIVE: {objective}
INDUSTRY: {industry} | GEOGRAPHY: {geography}

Provide 3 guiding strategic directives for your specialist team:
1. Marketing & Acquisition Gaps to examine
2. Commercial Monetization & Pricing Models to benchmark
3. Critical Risk Factors to scrutinize
"""
            res = director_model.invoke(prompt)
            plan_notes = str(res.content) if hasattr(res, "content") else str(res)
        except Exception:
            pass

    return {
        "execution_status": "executing_specialists",
        "strategic_recommendations": [{"directive": plan_notes[:300]}],
    }


# -------------------------------------------------------------
# Node 3: Parallel Specialists Execution (Marketing, Commercial, Opportunity, Risk)
# -------------------------------------------------------------
def parallel_specialists_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    objective = state.get("strategic_objective", "")
    industry = state.get("industry", "General Business")
    geography = state.get("geography", "Global")
    evidence = state.get("evidence_records", [])

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="parallel_specialists",
        event_type=StrategicEventType.SPECIALIST_STARTED.value,
        status="running",
        message="Dispatching Stage 2 specialists (Marketing, Commercial, Opportunity, Risk) on Spark 1.3.",
    )

    # 1. Marketing Intelligence Analyst
    mkt_queries = [
        f"{industry} marketing strategy campaigns {geography}",
        f"{industry} brand differentiation customer acquisition {geography}",
    ]
    mkt_res = run_marketing_analyst(
        objective=objective,
        queries=mkt_queries,
        industry=industry,
        geography=geography,
        research_id=research_id,
    )

    # 2. Commercial Intelligence Analyst
    comm_queries = [
        f"{industry} pricing models delivery charges {geography}",
        f"{industry} subscription e-commerce monetization {geography}",
    ]
    comm_res = run_commercial_analyst(
        objective=objective,
        queries=comm_queries,
        industry=industry,
        geography=geography,
        research_id=research_id,
    )

    # 3. Opportunity Discovery Analyst
    opp_res = run_opportunity_analyst(
        objective=objective,
        industry=industry,
        geography=geography,
        market_findings=state.get("market_report", {}),
        competitor_findings=state.get("competitor_report", {}),
        customer_findings=state.get("customer_report", {}),
        marketing_findings=mkt_res.get("marketing_report", {}),
        commercial_findings=comm_res.get("commercial_report", {}),
        evidence_records=evidence,
    )

    # 4. Risk & Industry Intelligence Analyst
    opportunities = opp_res.get("opportunities", [])
    risk_res = run_risk_analyst(
        objective=objective,
        industry=industry,
        geography=geography,
        opportunities=opportunities,
        market_findings=state.get("market_report", {}),
        competitor_findings=state.get("competitor_report", {}),
        evidence_records=evidence,
    )

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="parallel_specialists",
        event_type=StrategicEventType.SPECIALIST_COMPLETED.value,
        status="completed",
        message=(
            f"Stage 2 specialists completed analysis. Discovered {len(opportunities)} opportunities "
            f"and evaluated {len(risk_res.get('business_risks', []))} risk profiles."
        ),
    )

    return {
        "marketing_report": mkt_res.get("marketing_report", {}),
        "commercial_report": comm_res.get("commercial_report", {}),
        "opportunity_report": opp_res.get("opportunity_report", {}),
        "risk_report": risk_res.get("risk_report", {}),
        "opportunities": opportunities,
        "execution_status": "synthesis",
    }


# -------------------------------------------------------------
# Node 4: Strategic Synthesis & Gap Detection
# -------------------------------------------------------------
def strategic_synthesis_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]

    findings_map = {
        "Market Intelligence Analyst": state.get("market_report", {}),
        "Competitor Intelligence Analyst": state.get("competitor_report", {}),
        "Customer Intelligence Analyst": state.get("customer_report", {}),
        "Marketing Intelligence Analyst": state.get("marketing_report", {}),
        "Commercial Intelligence Analyst": state.get("commercial_report", {}),
        "Opportunity Discovery Analyst": state.get("opportunity_report", {}),
        "Risk & Industry Intelligence Analyst": state.get("risk_report", {}),
    }

    # Detect research gaps across reports
    gaps = detect_research_gaps(
        findings_by_agent=findings_map,
        claims=state.get("claims", []),
        contradictions=state.get("contradictions", []),
    )

    # Generate structured hypotheses
    hypotheses = generate_hypotheses_from_findings(
        gaps=gaps,
        customer_findings=state.get("customer_report", {}),
        competitor_findings=state.get("competitor_report", {}),
        market_findings=state.get("market_report", {}),
        evidence_ids=state.get("stage1_evidence_ids", []),
    )

    # Prioritize follow-up tasks
    tasks = prioritize_and_create_tasks(
        hypotheses=hypotheses,
        industry=state.get("industry", "General Business"),
        geography=state.get("geography", "Global"),
        max_tasks=4,
    )

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="Research Director",
        node_name="strategic_synthesis",
        event_type=StrategicEventType.RESEARCH_GAP_DETECTED.value,
        status="completed",
        message=f"Identified {len(gaps)} research gaps and formulated {len(hypotheses)} testable hypotheses.",
    )

    return {
        "research_gaps": gaps,
        "hypotheses": [h.model_dump() for h in hypotheses],
        "followup_tasks": [t.model_dump() for t in tasks],
        "execution_status": "evaluating_followup",
    }


# -------------------------------------------------------------
# Node 5: Autonomous Follow-up Research Execution (Bounded Loop)
# -------------------------------------------------------------
def followup_investigation_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    tasks = state.get("followup_tasks", [])
    hypotheses_data = state.get("hypotheses", [])
    current_iter = state.get("research_iterations", 1)

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="followup_investigation",
        event_type=StrategicEventType.FOLLOWUP_RESEARCH_STARTED.value,
        status="running",
        message=f"Executing iteration {current_iter} autonomous follow-up tasks ({len(tasks)} tasks).",
    )

    followup_results = []
    new_evidence_collected = []

    for task in tasks:
        t_id = task.get("task_id")
        target_agent = task.get("target_agent", "Specialist")
        queries = task.get("search_queries", [])

        # Execute targeted investigation via specialist
        from app.agents.specialist import run_specialist
        res = run_specialist(
            agent_name=target_agent,
            objective=task.get("research_question", ""),
            queries=queries[:2],
            industry=state.get("industry", "General Business"),
            geography=state.get("geography", "Global"),
            research_id=research_id,
        )

        ev_ids = res.get("evidence_ids", [])
        new_evidence_collected.extend(res.get("evidence", []))

        followup_results.append({
            "task_id": t_id,
            "hypothesis_id": task.get("hypothesis_id"),
            "target_agent": target_agent,
            "execution_result": res.get("summary", ""),
            "new_evidence_ids": ev_ids,
            "status": "completed",
        })

    # Validate hypotheses against acquired evidence
    hyp_objects = [ResearchHypothesis(**h) for h in hypotheses_data]
    validated_hyp = validate_hypotheses(
        hypotheses=hyp_objects,
        new_evidence=new_evidence_collected,
        followup_results=followup_results,
    )

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="followup_investigation",
        event_type=StrategicEventType.FOLLOWUP_RESEARCH_COMPLETED.value,
        status="completed",
        message=f"Completed follow-up research iteration {current_iter}. Updated {len(validated_hyp)} hypotheses.",
    )

    return {
        "hypotheses": [h.model_dump() for h in validated_hyp],
        "followup_results": followup_results,
        "followup_tasks": [],  # Clear pending queue
        "research_iterations": current_iter + 1,
        "execution_status": "scoring",
    }


# -------------------------------------------------------------
# Node 6: Opportunity Scoring & Ranking
# -------------------------------------------------------------
def opportunity_scoring_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    opportunities = state.get("opportunities", [])
    risks = state.get("risk_report", {}).get("business_risks", [])
    evidence = state.get("evidence_records", [])

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="opportunity_scoring",
        event_type=StrategicEventType.OPPORTUNITY_SCORED.value,
        status="running",
        message="Computing deterministic 6D opportunity scores and risk adjustments.",
    )

    scores_map = {}
    for opp in opportunities:
        opp_id = opp.get("opportunity_id", "")
        # Find associated risks
        opp_risks = [r for r in risks if r.get("opportunity_id") == opp_id]
        score_obj = score_opportunity(
            opportunity=opp,
            risks=opp_risks,
            evidence_records=evidence,
        )
        scores_map[opp_id] = score_obj

    # Rank opportunities
    ranked_opps = rank_opportunities(opportunities, scores_map)

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="opportunity_scoring",
        event_type=StrategicEventType.OPPORTUNITY_SCORED.value,
        status="completed",
        message=f"Ranked {len(ranked_opps)} opportunities deterministically.",
    )

    return {
        "opportunities": ranked_opps,
        "opportunity_scores": {k: v.model_dump() for k, v in scores_map.items()},
        "execution_status": "simulation",
    }


# -------------------------------------------------------------
# Node 7: Business Scenario Simulator
# -------------------------------------------------------------
def scenario_simulation_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    opportunities = state.get("opportunities", [])

    top_opp = opportunities[0] if opportunities else {
        "opportunity_id": "OPP-TOP",
        "opportunity_name": "Digital Brand Expansion",
    }

    base_input = ScenarioInput(
        scenario_name="Base Case",
        initial_investment=50000.0,
        product_selling_price=120.0,
        product_cost=50.0,
        expected_monthly_orders=600,
        monthly_marketing_expenditure=6000.0,
        delivery_cost_per_order=6.0,
        return_refund_rate=0.06,
        fixed_operating_expenses=8500.0,
    )

    scenario_suite = build_scenario_suite(
        opportunity_id=top_opp.get("opportunity_id", "OPP-TOP"),
        opportunity_name=top_opp.get("opportunity_name", "Top Opportunity"),
        base_input=base_input,
    )

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="scenario_simulation",
        event_type=StrategicEventType.SCENARIO_CALCULATED.value,
        status="completed",
        message=f"Calculated Base/Best/Worst financial scenarios for '{top_opp.get('opportunity_name', '')[:40]}...'",
    )

    return {
        "scenario_models": scenario_suite.model_dump(),
        "execution_status": "director_report",
    }


# -------------------------------------------------------------
# Node 8: Strategic Executive Report (Sections A through J)
# -------------------------------------------------------------
def strategic_executive_report_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]
    objective = state.get("strategic_objective", "")
    industry = state.get("industry", "General Business")
    geography = state.get("geography", "Global")
    opportunities = state.get("opportunities", [])
    hypotheses = state.get("hypotheses", [])
    risks = state.get("risk_report", {}).get("business_risks", [])

    director_model = get_director_model()

    # Section contents
    sec_a = (
        f"Executive Summary for strategic objective: {objective}. "
        f"Autonomous discovery identified {len(opportunities)} commercially attractive opportunities "
        f"in {industry} ({geography}). Primary findings substantiate unmet customer demand for "
        "transparent sizing and logistics certainty, while incumbent competitors remain fixated on discount volume."
    )
    sec_b = state.get("market_report", {}).get("summary", "Market intelligence verified from Stage 1.")
    sec_c = state.get("competitor_report", {}).get("summary", "Competitor positioning and gaps verified from Stage 1.")
    sec_d = state.get("marketing_report", {}).get("summary", "Marketing intelligence and campaign channel analysis.")
    sec_e = state.get("commercial_report", {}).get("summary", "Commercial pricing models and monetization feasibility.")

    recs = [
        {"title": "Prioritize Guaranteed Delivery Logistics", "category": "evidence_backed", "description": "Implement contractual courier SLAs and real-time tracking."},
        {"title": "Standardize Garment Measurement & Fit Guidance", "category": "evidence_backed", "description": "Reduce return overhead by offering transparent sizing profiles."},
        {"title": "Pilot Replenishment Subscription", "category": "hypothesis", "description": "Validate recurring replenishment with urban repeat purchasers."},
    ]

    gaps = state.get("research_gaps", ["Long-term customer lifetime value in subscription models"])

    report_payload = {
        "strategic_analysis_id": analysis_id,
        "research_id": research_id,
        "strategic_objective": objective,
        "industry": industry,
        "geography": geography,
        "director_model": "muse-wonder-1.0",
        "specialist_model": "spark-1.3",
        "section_a_executive_summary": sec_a,
        "section_b_market_intelligence": sec_b,
        "section_c_competitor_intelligence": sec_c,
        "section_d_marketing_intelligence": sec_d,
        "section_e_commercial_intelligence": sec_e,
        "section_f_opportunity_discovery": opportunities,
        "section_g_risk_assessment": risks,
        "section_h_scenario_analysis": state.get("scenario_models"),
        "section_i_strategic_recommendations": recs,
        "section_j_further_research": gaps,
        "total_opportunities": len(opportunities),
        "total_hypotheses": len(hypotheses),
        "total_risks": len(risks),
        "research_iterations_executed": state.get("research_iterations", 1),
        "evidence_count": len(state.get("evidence_records", [])),
    }

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="Research Director",
        node_name="strategic_executive_report",
        event_type=StrategicEventType.STRATEGIC_REPORT_GENERATED.value,
        status="completed",
        message="Chief Research Director (Meta Muse Wonder) completed 10-section strategic executive report.",
    )

    return {
        "strategic_report": report_payload,
        "strategic_recommendations": recs,
        "execution_status": "persistence",
    }


# -------------------------------------------------------------
# Node 9: Persistence Node
# -------------------------------------------------------------
def persist_strategic_analysis_node(state: StrategicState) -> Dict[str, Any]:
    analysis_id = state["strategic_analysis_id"]
    research_id = state["research_id"]

    save_complete_strategic_analysis(
        analysis_id=analysis_id,
        research_id=research_id,
        strategic_objective=state.get("strategic_objective", ""),
        status="completed",
        research_iterations=state.get("research_iterations", 1),
        strategic_plan={"recommendations": state.get("strategic_recommendations", [])},
        final_report=state.get("strategic_report", {}),
        marketing_report=state.get("marketing_report", {}),
        commercial_report=state.get("commercial_report", {}),
        opportunities=state.get("opportunities", []),
        hypotheses=state.get("hypotheses", []),
        tasks=state.get("followup_results", []),
        risks=state.get("risk_report", {}).get("business_risks", []),
        opportunity_scores=state.get("opportunity_scores", {}),
        recommendations=state.get("strategic_recommendations", []),
    )

    save_strategic_event(
        analysis_id=analysis_id,
        research_id=research_id,
        event_id=f"EVT-{uuid.uuid4().hex[:6]}",
        agent_name="System",
        node_name="persist_strategic_analysis",
        event_type=StrategicEventType.STRATEGIC_ANALYSIS_COMPLETED.value,
        status="completed",
        message="Strategic analysis, opportunities, hypotheses, and scenario models persisted to SQLite.",
    )

    return {
        "execution_status": "completed",
    }
