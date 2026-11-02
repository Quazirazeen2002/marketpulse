"""
Repository module for SQLite persistence of all MARKETPULSE research entities.
Handles safe insertion, queries, historical run retrieval, and comparison.
"""

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select, desc, func

from app.database.db import engine
from app.database.models import (
    ResearchRun,
    ResearchAgentRun,
    SourceDocumentRecord,
    SourceQualityRecord,
    EvidenceRecord,
    ResearchClaimRecord,
    ContradictionRecordModel,
    ExecutionEventRecord,
    ResearchGapRecord,
    ResearchArtifact,
    StrategicAnalysisRecord,
    MarketingIntelligenceRecord,
    CommercialIntelligenceRecord,
    OpportunityDbRecord,
    OpportunityEvidenceLink,
    ResearchHypothesisRecord,
    FollowupResearchTaskRecord,
    RiskAssessmentRecord,
    OpportunityScoreRecord,
    ScenarioModelRecord,
    ScenarioInputRecord,
    StrategicRecommendationRecord,
    StrategicExecutionEventRecord,
)


def save_execution_event(
    run_id: str,
    event_id: str,
    agent_name: str,
    node_name: str,
    event_type: str,
    status: str,
    message: str,
    duration_ms: Optional[int] = None,
) -> None:
    """Persist a single execution event in SQLite."""
    try:
        with Session(engine) as session:
            record = ExecutionEventRecord(
                event_id=event_id,
                run_id=run_id,
                agent_name=agent_name,
                node_name=node_name,
                event_type=event_type,
                status=status,
                message=message,
                duration_ms=duration_ms,
                timestamp=datetime.now(timezone.utc),
            )
            session.add(record)
            session.commit()
    except Exception as exc:
        print(f"[REPOSITORY WARNING] Failed to persist event {event_id}: {exc}")


def to_jsonable(obj: Any) -> Any:
    """Recursively convert Pydantic models, Enums, and non-primitives to JSON-serializable types."""
    from enum import Enum
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


def save_complete_research_run(state: Dict[str, Any]) -> str:
    """
    Persist all entities from a completed or partial research run.
    Safely saves run, agent runs, source documents, qualities,
    evidence records, claims, contradictions, gaps, and artifacts.
    """
    research_id = state.get("research_id", "")
    if not research_id:
        return ""

    final_report = to_jsonable(state.get("final_report", {}))
    research_plan = to_jsonable(state.get("research_plan", {}))
    status_dimensions = state.get("status_dimensions", {})

    with Session(engine) as session:
        # Check if research run already exists to update or insert
        existing_run = session.exec(
            select(ResearchRun).where(ResearchRun.id == research_id)
        ).first()

        sources = state.get("sources", [])
        evidence_list = state.get("evidence_registry", [])
        claims = state.get("claims", [])
        contradictions = state.get("contradictions", [])
        gaps = state.get("research_gaps", [])

        full_text_count = sum(
            1 for s in sources if getattr(s, "extraction_status", "") == "retrieved_full_text"
            or (isinstance(s, dict) and s.get("extraction_status") == "retrieved_full_text")
        )
        snippet_only_count = sum(
            1 for s in sources if getattr(s, "extraction_status", "") == "snippet_only"
            or (isinstance(s, dict) and s.get("extraction_status") == "snippet_only")
        )
        verified_claims_count = sum(
            1 for c in claims if getattr(c, "verification_status", "") == "supported"
            or (isinstance(c, dict) and c.get("verification_status") == "supported")
        )
        unverified_claims_count = sum(
            1 for c in claims if getattr(c, "verification_status", "") in ("unverified", "insufficient_evidence")
            or (isinstance(c, dict) and c.get("verification_status") in ("unverified", "insufficient_evidence"))
        )

        exec_status = status_dimensions.get("execution_status", state.get("research_status", "completed"))
        quality_status = status_dimensions.get("research_quality", "moderate")
        verif_status = status_dimensions.get("verification_status", "partially_verified")

        if existing_run:
            existing_run.status = exec_status
            existing_run.research_quality = quality_status
            existing_run.verification_status = verif_status
            existing_run.total_sources = len(sources)
            existing_run.full_text_sources = full_text_count
            existing_run.snippet_only_sources = snippet_only_count
            existing_run.verified_claims = verified_claims_count
            existing_run.unverified_claims = unverified_claims_count
            existing_run.contradictions_count = len(contradictions)
            existing_run.research_plan = research_plan
            existing_run.final_report = final_report
            existing_run.completed_at = datetime.now(timezone.utc)
            session.add(existing_run)
        else:
            new_run = ResearchRun(
                id=research_id,
                objective=state.get("research_objective", ""),
                industry=state.get("industry", ""),
                geography=state.get("geography", ""),
                time_horizon=state.get("time_horizon", "Current (Real-time)"),
                status=exec_status,
                research_quality=quality_status,
                verification_status=verif_status,
                total_sources=len(sources),
                full_text_sources=full_text_count,
                snippet_only_sources=snippet_only_count,
                verified_claims=verified_claims_count,
                unverified_claims=unverified_claims_count,
                contradictions_count=len(contradictions),
                research_plan=research_plan,
                final_report=final_report,
                created_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc),
            )
            session.add(new_run)

        session.flush()

        # 2. Persist Specialist Agent Runs & Artifacts
        specialist_reports = [
            ("Market Intelligence Analyst", state.get("market_report", {})),
            ("Competitor Intelligence Analyst", state.get("competitor_report", {})),
            ("Customer Intelligence Analyst", state.get("customer_report", {})),
        ]

        for agent_name, rep in specialist_reports:
            if not rep:
                continue
            rep_dict = to_jsonable(rep if isinstance(rep, dict) else rep.model_dump())
            session.add(
                ResearchAgentRun(
                    research_id=research_id,
                    agent_name=rep_dict.get("agent_name", agent_name),
                    status=rep_dict.get("research_status", "completed"),
                    summary=rep_dict.get("summary", ""),
                    evidence_count=len(rep_dict.get("evidence_ids", [])),
                )
            )
            session.add(
                ResearchArtifact(
                    research_id=research_id,
                    agent_name=rep_dict.get("agent_name", agent_name),
                    artifact_type="specialist_report",
                    content=rep_dict,
                )
            )

        # 3. Persist Source Documents & Quality Assessments
        source_qualities = state.get("source_qualities", {})
        seen_source_ids = set()

        for src in sources:
            s_dict = src if isinstance(src, dict) else src.model_dump()
            src_id = s_dict.get("source_id", "")
            if not src_id or src_id in seen_source_ids:
                continue
            seen_source_ids.add(src_id)

            session.add(
                SourceDocumentRecord(
                    source_id=src_id,
                    research_id=research_id,
                    url=s_dict.get("url", ""),
                    canonical_url=s_dict.get("canonical_url"),
                    title=s_dict.get("title", ""),
                    publisher=s_dict.get("publisher", ""),
                    author=s_dict.get("author"),
                    publication_date=s_dict.get("publication_date"),
                    extraction_status=s_dict.get("extraction_status", "snippet_only"),
                    extracted_text=s_dict.get("extracted_text", "")[:100000],  # Bound text storage
                    content_hash=s_dict.get("content_hash", ""),
                    content_type=s_dict.get("content_type", "text/html"),
                    duplicate_group_id=s_dict.get("duplicate_group_id"),
                    is_canonical=s_dict.get("is_canonical", True),
                    http_status=s_dict.get("http_status"),
                    search_provider=s_dict.get("search_provider", "tavily"),
                )
            )

            # Check if there is a quality assessment for this source
            qa = source_qualities.get(src_id)
            if qa:
                qa_dict = qa if isinstance(qa, dict) else qa.model_dump()
                session.add(
                    SourceQualityRecord(
                        source_id=src_id,
                        research_id=research_id,
                        credibility_score=qa_dict.get("credibility_score", 0.0),
                        relevance_score=qa_dict.get("relevance_score", 0.0),
                        freshness_score=qa_dict.get("freshness_score", 0.0),
                        completeness_score=qa_dict.get("completeness_score", 0.0),
                        specificity_score=qa_dict.get("specificity_score", 0.0),
                        composite_score=qa_dict.get("composite_score", 0.0),
                        scoring_rationale=qa_dict.get("scoring_rationale", ""),
                    )
                )

        # 4. Persist Evidence Records
        seen_ev_ids = set()
        for ev in evidence_list:
            ev_dict = ev if isinstance(ev, dict) else ev.model_dump()
            e_id = ev_dict.get("evidence_id", "")
            if not e_id or e_id in seen_ev_ids:
                continue
            seen_ev_ids.add(e_id)

            session.add(
                EvidenceRecord(
                    evidence_id=e_id,
                    source_id=ev_dict.get("source_id"),
                    research_id=research_id,
                    is_cited=ev_dict.get("is_cited", False),
                    search_query=ev_dict.get("search_query", ""),
                    source_url=ev_dict.get("source_url", ""),
                    source_title=ev_dict.get("source_title", ""),
                    publisher=ev_dict.get("publisher", ""),
                    published_at=ev_dict.get("published_at"),
                    supporting_excerpt=ev_dict.get("supporting_excerpt", "") or ev_dict.get("exact_excerpt", ""),
                    source_type=ev_dict.get("source_type", "tavily_search"),
                    search_provider=ev_dict.get("search_provider", "tavily"),
                    extraction_status=ev_dict.get("extraction_status", "snippet_only"),
                    relevance_score=ev_dict.get("relevance_score", 0.0),
                    reliability_score=ev_dict.get("reliability_score", 0.0),
                    content_hash=ev_dict.get("content_hash", e_id),
                    duplicate_group_id=ev_dict.get("duplicate_group_id"),
                )
            )

        # 5. Persist Research Claims
        seen_claim_ids = set()
        for clm in claims:
            c_dict = clm if isinstance(clm, dict) else clm.model_dump()
            c_id = c_dict.get("claim_id", "")
            if not c_id or c_id in seen_claim_ids:
                continue
            seen_claim_ids.add(c_id)

            session.add(
                ResearchClaimRecord(
                    claim_id=c_id,
                    research_id=research_id,
                    agent_name=c_dict.get("agent_name", "Specialist"),
                    claim_text=c_dict.get("claim_text", "") or c_dict.get("claim", ""),
                    claim_type=c_dict.get("claim_type", "fact"),
                    verification_status=c_dict.get("verification_status", "unverified"),
                    confidence_score=c_dict.get("confidence_score", 0.0),
                    verification_rationale=c_dict.get("verification_rationale", "") or c_dict.get("reasoning", ""),
                    is_hypothesis=c_dict.get("is_hypothesis", False),
                )
            )

        # 6. Persist Contradiction Records
        for con in contradictions:
            con_dict = con if isinstance(con, dict) else con.model_dump()
            session.add(
                ContradictionRecordModel(
                    contradiction_id=con_dict.get("contradiction_id", ""),
                    research_id=research_id,
                    topic=con_dict.get("topic", "Market Dynamics"),
                    claim_a_id=con_dict.get("claim_a_id", ""),
                    claim_a_text=con_dict.get("claim_a_text", ""),
                    claim_b_id=con_dict.get("claim_b_id", ""),
                    claim_b_text=con_dict.get("claim_b_text", ""),
                    conflict_summary=con_dict.get("conflict_summary", ""),
                    resolution_status=con_dict.get("resolution_status", "unresolved"),
                )
            )

        # 7. Persist Research Gaps
        for gap in gaps:
            gap_desc = gap if isinstance(gap, str) else gap.get("gap_description", str(gap))
            session.add(
                ResearchGapRecord(
                    research_id=research_id,
                    gap_description=gap_desc,
                    agent_name="Research Director",
                )
            )

        session.commit()

    return research_id


def list_research_runs(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve list of historical research runs sorted by created_at desc."""
    with Session(engine) as session:
        statement = select(ResearchRun).order_by(desc(ResearchRun.created_at)).limit(limit)
        runs = session.exec(statement).all()
        return [run.model_dump() for run in runs]


def get_research_run(run_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full details of a single research run."""
    with Session(engine) as session:
        statement = select(ResearchRun).where(ResearchRun.id == run_id)
        run = session.exec(statement).first()
        return run.model_dump() if run else None


def get_run_sources(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve all source documents and their quality assessments for a run."""
    with Session(engine) as session:
        sources = session.exec(
            select(SourceDocumentRecord).where(SourceDocumentRecord.research_id == run_id)
        ).all()
        qualities = {
            q.source_id: q.model_dump()
            for q in session.exec(
                select(SourceQualityRecord).where(SourceQualityRecord.research_id == run_id)
            ).all()
        }

        results = []
        for s in sources:
            s_dict = s.model_dump()
            s_dict["quality"] = qualities.get(s.source_id, {})
            results.append(s_dict)
        return results


def get_run_evidence(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve all evidence records for a given run."""
    with Session(engine) as session:
        evs = session.exec(
            select(EvidenceRecord).where(EvidenceRecord.research_id == run_id)
        ).all()
        return [e.model_dump() for e in evs]


def get_run_claims(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve all claims and their verification details for a run."""
    with Session(engine) as session:
        claims = session.exec(
            select(ResearchClaimRecord).where(ResearchClaimRecord.research_id == run_id)
        ).all()
        return [c.model_dump() for c in claims]


def get_run_contradictions(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve all contradictions flagged in a run."""
    with Session(engine) as session:
        cons = session.exec(
            select(ContradictionRecordModel).where(ContradictionRecordModel.research_id == run_id)
        ).all()
        return [c.model_dump() for c in cons]


def get_run_events(run_id: str) -> List[Dict[str, Any]]:
    """Retrieve all execution events for a run."""
    with Session(engine) as session:
        events = session.exec(
            select(ExecutionEventRecord).where(ExecutionEventRecord.run_id == run_id).order_by(ExecutionEventRecord.timestamp)
        ).all()
        return [e.model_dump() for e in events]


def get_run_gaps(run_id: str) -> List[str]:
    """Retrieve research gaps for a run."""
    with Session(engine) as session:
        gaps = session.exec(
            select(ResearchGapRecord).where(ResearchGapRecord.research_id == run_id)
        ).all()
        return [g.gap_description for g in gaps]


def compare_runs(run_id_a: str, run_id_b: str) -> Dict[str, Any]:
    """Compare two research runs across sources, claims, quality, and findings."""
    run_a = get_research_run(run_id_a)
    run_b = get_research_run(run_id_b)

    if not run_a or not run_b:
        return {"error": "One or both runs not found."}

    sources_a = get_run_sources(run_id_a)
    sources_b = get_run_sources(run_id_b)

    claims_a = get_run_claims(run_id_a)
    claims_b = get_run_claims(run_id_b)

    contradictions_a = get_run_contradictions(run_id_a)
    contradictions_b = get_run_contradictions(run_id_b)

    return {
        "run_a": {
            "id": run_a["id"],
            "objective": run_a["objective"],
            "status": run_a["status"],
            "quality": run_a["research_quality"],
            "verification": run_a["verification_status"],
            "total_sources": len(sources_a),
            "total_claims": len(claims_a),
            "verified_claims": sum(1 for c in claims_a if c["verification_status"] == "supported"),
            "contradictions": len(contradictions_a),
            "created_at": run_a["created_at"],
        },
        "run_b": {
            "id": run_b["id"],
            "objective": run_b["objective"],
            "status": run_b["status"],
            "quality": run_b["research_quality"],
            "verification": run_b["verification_status"],
            "total_sources": len(sources_b),
            "total_claims": len(claims_b),
            "verified_claims": sum(1 for c in claims_b if c["verification_status"] == "supported"),
            "contradictions": len(contradictions_b),
            "created_at": run_b["created_at"],
        },
        "deltas": {
            "source_difference": len(sources_b) - len(sources_a),
            "claims_difference": len(claims_b) - len(claims_a),
            "verified_claims_difference": (
                sum(1 for c in claims_b if c["verification_status"] == "supported")
                - sum(1 for c in claims_a if c["verification_status"] == "supported")
            ),
        },
    }


# ---------------------------------------------------------
# STAGE 2 STRATEGIC PERSISTENCE & RETRIEVAL
# ---------------------------------------------------------

def save_strategic_event(
    analysis_id: str,
    research_id: str,
    event_id: str,
    agent_name: str,
    node_name: str,
    event_type: str,
    status: str,
    message: str,
    duration_ms: Optional[int] = None,
) -> None:
    """Persist a single strategic execution event."""
    try:
        with Session(engine) as session:
            record = StrategicExecutionEventRecord(
                event_id=event_id,
                analysis_id=analysis_id,
                research_id=research_id,
                agent_name=agent_name,
                node_name=node_name,
                event_type=event_type,
                status=status,
                message=message,
                duration_ms=duration_ms,
                timestamp=datetime.now(timezone.utc),
            )
            session.add(record)
            session.commit()
    except Exception as exc:
        print(f"[STRATEGIC EVENT PERSISTENCE ERROR] {exc}")


def save_complete_strategic_analysis(
    analysis_id: str,
    research_id: str,
    strategic_objective: str,
    status: str = "completed",
    research_iterations: int = 1,
    strategic_plan: Optional[Dict[str, Any]] = None,
    final_report: Optional[Dict[str, Any]] = None,
    marketing_report: Optional[Dict[str, Any]] = None,
    commercial_report: Optional[Dict[str, Any]] = None,
    opportunities: Optional[List[Dict[str, Any]]] = None,
    hypotheses: Optional[List[Dict[str, Any]]] = None,
    tasks: Optional[List[Dict[str, Any]]] = None,
    risks: Optional[List[Dict[str, Any]]] = None,
    opportunity_scores: Optional[Dict[str, Any]] = None,
    recommendations: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Atomically persist a complete strategic analysis and all child records."""
    opportunities = opportunities or []
    hypotheses = hypotheses or []
    tasks = tasks or []
    risks = risks or []
    opportunity_scores = opportunity_scores or {}
    recommendations = recommendations or []

    with Session(engine) as session:
        # 1. StrategicAnalysisRecord
        existing_analysis = session.get(StrategicAnalysisRecord, analysis_id)
        if not existing_analysis:
            analysis_rec = StrategicAnalysisRecord(
                id=analysis_id,
                research_id=research_id,
                strategic_objective=strategic_objective,
                status=status,
                research_iterations=research_iterations,
                total_hypotheses=len(hypotheses),
                total_opportunities=len(opportunities),
                total_risks=len(risks),
                strategic_plan=strategic_plan or {},
                final_report=final_report or {},
                completed_at=datetime.now(timezone.utc) if status == "completed" else None,
            )
            session.add(analysis_rec)
        else:
            existing_analysis.status = status
            existing_analysis.research_iterations = research_iterations
            existing_analysis.total_hypotheses = len(hypotheses)
            existing_analysis.total_opportunities = len(opportunities)
            existing_analysis.total_risks = len(risks)
            existing_analysis.final_report = final_report or {}
            existing_analysis.completed_at = datetime.now(timezone.utc) if status == "completed" else None
            session.add(existing_analysis)

        # 2. Marketing Intelligence
        if marketing_report:
            mkt_rec = MarketingIntelligenceRecord(
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                brand_intelligence=marketing_report.get("brand_intelligence", {}),
                campaign_intelligence=marketing_report.get("campaign_intelligence", {}),
                channel_intelligence=marketing_report.get("channel_intelligence", {}),
                marketing_gaps={"gaps": marketing_report.get("marketing_gaps", []), "unknowns": marketing_report.get("unknown_metrics", [])},
                summary=marketing_report.get("summary", ""),
            )
            session.add(mkt_rec)

        # 3. Commercial Intelligence
        if commercial_report:
            comm_rec = CommercialIntelligenceRecord(
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                pricing_structures={"structures": commercial_report.get("pricing_structures", [])},
                monetization_models={"models": commercial_report.get("monetization_models", [])},
                public_delivery_charges={"charges": commercial_report.get("public_delivery_charges", [])},
                pricing_gaps={"gaps": commercial_report.get("pricing_gaps", [])},
                commercial_feasibility=commercial_report.get("commercial_feasibility", ""),
                summary=commercial_report.get("summary", ""),
            )
            session.add(comm_rec)

        # 4. Opportunities & Evidence Links
        for opp in opportunities:
            opp_id = opp.get("opportunity_id", "")
            opp_rec = OpportunityDbRecord(
                opportunity_id=opp_id,
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                opportunity_name=opp.get("opportunity_name", ""),
                problem_statement=opp.get("problem_statement", ""),
                target_customer=opp.get("target_customer", ""),
                market_segment=opp.get("market_segment", ""),
                proposed_solution=opp.get("proposed_solution", ""),
                commercial_model=opp.get("commercial_model", ""),
                expected_customer_value=opp.get("expected_customer_value", ""),
                competitive_differentiation=opp.get("competitive_differentiation", ""),
                originating_hypothesis_id=opp.get("originating_hypothesis_id"),
                status=opp.get("status", "discovered"),
            )
            session.add(opp_rec)

            # Link evidence
            for eid in opp.get("supporting_evidence_ids", []):
                session.add(OpportunityEvidenceLink(
                    opportunity_id=opp_id,
                    strategic_analysis_id=analysis_id,
                    research_id=research_id,
                    evidence_id=eid,
                    is_supporting=True,
                ))

            # Store score if available
            score_data = opportunity_scores.get(opp_id)
            if score_data:
                s_dict = score_data if isinstance(score_data, dict) else score_data.model_dump()
                session.add(OpportunityScoreRecord(
                    opportunity_id=opp_id,
                    strategic_analysis_id=analysis_id,
                    research_id=research_id,
                    raw_score=s_dict.get("raw_score", 0.0),
                    risk_adjusted_score=s_dict.get("risk_adjusted_score", 0.0),
                    component_scores=s_dict.get("component_scores", {}),
                    dimension_weights=s_dict.get("dimension_weights", {}),
                    scoring_rationale=s_dict.get("scoring_rationale", {}),
                ))

        # 5. Hypotheses
        for hyp in hypotheses:
            h_id = hyp.get("hypothesis_id", "")
            session.add(ResearchHypothesisRecord(
                hypothesis_id=h_id,
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                description=hyp.get("description", ""),
                validation_status=hyp.get("validation_status", "proposed"),
                confidence_assessment=hyp.get("confidence_assessment", 0.5),
                final_disposition=hyp.get("final_disposition"),
                originating_findings={"findings": hyp.get("originating_findings", [])},
            ))

        # 6. Follow-up Tasks
        for t in tasks:
            t_id = t.get("task_id", "")
            session.add(FollowupResearchTaskRecord(
                task_id=t_id,
                hypothesis_id=t.get("hypothesis_id", ""),
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                target_agent=t.get("target_agent", ""),
                research_question=t.get("research_question", ""),
                priority=t.get("priority", 1),
                status=t.get("status", "completed"),
                execution_result=t.get("execution_result"),
            ))

        # 7. Risk Assessments
        for r in risks:
            r_id = r.get("risk_id", "")
            session.add(RiskAssessmentRecord(
                risk_id=r_id,
                opportunity_id=r.get("opportunity_id"),
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                risk_description=r.get("risk_description", ""),
                risk_category=r.get("risk_category", "operational"),
                likelihood=r.get("likelihood", "medium"),
                impact=r.get("impact", "medium"),
                likelihood_score=r.get("likelihood_score", 0.5),
                impact_score=r.get("impact_score", 0.5),
                mitigation_strategy=r.get("mitigation_strategy", ""),
                residual_risk=r.get("residual_risk", ""),
            ))

        # 8. Recommendations
        for rec in recommendations:
            session.add(StrategicRecommendationRecord(
                strategic_analysis_id=analysis_id,
                research_id=research_id,
                title=rec.get("title", ""),
                description=rec.get("description", ""),
                category=rec.get("category", "evidence_backed"),
                supporting_evidence_ids={"evidence": rec.get("supporting_evidence_ids", [])},
            ))

        session.commit()


def get_strategic_analysis(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full strategic analysis record."""
    with Session(engine) as session:
        statement = select(StrategicAnalysisRecord).where(StrategicAnalysisRecord.id == analysis_id)
        record = session.exec(statement).first()
        if not record:
            return None
        return record.model_dump()


def list_strategic_analyses(research_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """List historical strategic analyses."""
    with Session(engine) as session:
        statement = select(StrategicAnalysisRecord).order_by(desc(StrategicAnalysisRecord.created_at)).limit(limit)
        if research_id:
            statement = statement.where(StrategicAnalysisRecord.research_id == research_id)
        records = session.exec(statement).all()
        return [r.model_dump() for r in records]


def get_strategic_opportunities(analysis_id: str) -> List[Dict[str, Any]]:
    """Retrieve all discovered opportunities and their scores for an analysis."""
    with Session(engine) as session:
        statement = select(OpportunityDbRecord).where(OpportunityDbRecord.strategic_analysis_id == analysis_id)
        opps = session.exec(statement).all()

        scores_stmt = select(OpportunityScoreRecord).where(OpportunityScoreRecord.strategic_analysis_id == analysis_id)
        scores = {s.opportunity_id: s.model_dump() for s in session.exec(scores_stmt).all()}

        results = []
        for opp in opps:
            opp_dict = opp.model_dump()
            score_data = scores.get(opp.opportunity_id)
            if score_data:
                opp_dict["raw_score"] = score_data.get("raw_score", 0.0)
                opp_dict["risk_adjusted_score"] = score_data.get("risk_adjusted_score", 0.0)
                opp_dict["component_scores"] = score_data.get("component_scores", {})
                opp_dict["scoring_rationale"] = score_data.get("scoring_rationale", {})
            results.append(opp_dict)

        results.sort(key=lambda x: x.get("risk_adjusted_score", 0.0), reverse=True)
        return results


def get_strategic_hypotheses(analysis_id: str) -> List[Dict[str, Any]]:
    """Retrieve all research hypotheses for an analysis."""
    with Session(engine) as session:
        statement = select(ResearchHypothesisRecord).where(ResearchHypothesisRecord.strategic_analysis_id == analysis_id)
        return [h.model_dump() for h in session.exec(statement).all()]


def get_strategic_risks(analysis_id: str) -> List[Dict[str, Any]]:
    """Retrieve all risk assessments for an analysis."""
    with Session(engine) as session:
        statement = select(RiskAssessmentRecord).where(RiskAssessmentRecord.strategic_analysis_id == analysis_id)
        return [r.model_dump() for r in session.exec(statement).all()]


def get_strategic_events(analysis_id: str) -> List[Dict[str, Any]]:
    """Retrieve execution events for an analysis."""
    with Session(engine) as session:
        statement = select(StrategicExecutionEventRecord).where(
            StrategicExecutionEventRecord.analysis_id == analysis_id
        ).order_by(StrategicExecutionEventRecord.timestamp)
        return [e.model_dump() for e in session.exec(statement).all()]


def save_scenario_simulation(
    strategic_analysis_id: str,
    research_id: str,
    opportunity_id: str,
    scenario_suite: Dict[str, Any],
) -> None:
    """Save business scenario simulation results."""
    with Session(engine) as session:
        for case_key in ("base_case", "best_case", "worst_case"):
            case_data = scenario_suite.get(case_key, {})
            if case_data:
                session.add(ScenarioModelRecord(
                    opportunity_id=opportunity_id,
                    strategic_analysis_id=strategic_analysis_id,
                    research_id=research_id,
                    scenario_name=case_data.get("scenario_name", case_key),
                    monthly_revenue=case_data.get("monthly_revenue", 0.0),
                    gross_profit=case_data.get("gross_profit", 0.0),
                    gross_margin_percent=case_data.get("gross_margin_percent", 0.0),
                    contribution_margin_percent=case_data.get("contribution_margin_percent", 0.0),
                    monthly_operating_profit=case_data.get("monthly_operating_profit", 0.0),
                    annual_operating_profit=case_data.get("annual_operating_profit", 0.0),
                    break_even_orders=case_data.get("break_even_orders", 0),
                    break_even_revenue=case_data.get("break_even_revenue", 0.0),
                    estimated_cash_requirement=case_data.get("estimated_cash_requirement", 0.0),
                    is_profitable=case_data.get("is_profitable", False),
                ))
        session.commit()


def get_stored_scenarios(strategic_analysis_id: str) -> List[Dict[str, Any]]:
    """Retrieve stored scenario models for an analysis."""
    with Session(engine) as session:
        statement = select(ScenarioModelRecord).where(
            ScenarioModelRecord.strategic_analysis_id == strategic_analysis_id
        )
        return [s.model_dump() for s in session.exec(statement).all()]


def get_opportunity_by_id(opportunity_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single opportunity by ID, including its score and evidence links."""
    with Session(engine) as session:
        statement = select(OpportunityDbRecord).where(OpportunityDbRecord.opportunity_id == opportunity_id)
        opp = session.exec(statement).first()
        if not opp:
            return None
        data = opp.model_dump()
        score_stmt = select(OpportunityScoreRecord).where(OpportunityScoreRecord.opportunity_id == opportunity_id)
        score = session.exec(score_stmt).first()
        if score:
            score_data = score.model_dump()
            data["raw_score"] = score_data.get("raw_score", 0.0)
            data["risk_adjusted_score"] = score_data.get("risk_adjusted_score", 0.0)
            data["component_scores"] = score_data.get("component_scores", {})
            data["dimension_weights"] = score_data.get("dimension_weights", {})
            data["scoring_rationale"] = score_data.get("scoring_rationale", {})
            data["missing_information"] = score_data.get("missing_information", [])
        # Fetch linked evidence
        links_stmt = select(OpportunityEvidenceLink).where(OpportunityEvidenceLink.opportunity_id == opportunity_id)
        links = session.exec(links_stmt).all()
        data["evidence_links"] = [link.model_dump() for link in links]
        return data


def get_marketing_intelligence(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve marketing intelligence record for a strategic analysis."""
    with Session(engine) as session:
        stmt = select(MarketingIntelligenceRecord).where(MarketingIntelligenceRecord.strategic_analysis_id == analysis_id)
        record = session.exec(stmt).first()
        return record.model_dump() if record else None


def get_commercial_intelligence(analysis_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve commercial intelligence record for a strategic analysis."""
    with Session(engine) as session:
        stmt = select(CommercialIntelligenceRecord).where(CommercialIntelligenceRecord.strategic_analysis_id == analysis_id)
        record = session.exec(stmt).first()
        return record.model_dump() if record else None


def get_overview_metrics() -> Dict[str, Any]:
    """Retrieve aggregate counts and statistics across the research platform."""
    with Session(engine) as session:
        total_runs = session.exec(select(func.count(ResearchRun.id))).one()
        completed_runs = session.exec(select(func.count(ResearchRun.id)).where(ResearchRun.status == "completed")).one()
        high_quality_runs = session.exec(select(func.count(ResearchRun.id)).where(ResearchRun.research_quality == "high")).one()
        total_sources = session.exec(select(func.count(SourceDocumentRecord.id))).one()
        total_evidence = session.exec(select(func.count(EvidenceRecord.id))).one()
        verified_claims = session.exec(select(func.count(ResearchClaimRecord.id)).where(ResearchClaimRecord.verification_status == "verified")).one()
        total_claims = session.exec(select(func.count(ResearchClaimRecord.id))).one()
        total_opportunities = session.exec(select(func.count(OpportunityDbRecord.id))).one()
        total_hypotheses = session.exec(select(func.count(ResearchHypothesisRecord.id))).one()
        total_risks = session.exec(select(func.count(RiskAssessmentRecord.id))).one()
        total_analyses = session.exec(select(func.count(StrategicAnalysisRecord.id))).one()

        # Recent runs
        recent_stmt = select(ResearchRun).order_by(desc(ResearchRun.created_at)).limit(5)
        recent_runs = [r.model_dump() for r in session.exec(recent_stmt).all()]

        return {
            "total_research_runs": total_runs,
            "completed_investigations": completed_runs,
            "high_quality_runs": high_quality_runs,
            "evidence_records": total_evidence,
            "verified_claims": verified_claims,
            "total_claims": total_claims,
            "discovered_opportunities": total_opportunities,
            "total_hypotheses": total_hypotheses,
            "total_risks": total_risks,
            "total_sources": total_sources,
            "total_strategic_analyses": total_analyses,
            "recent_runs": recent_runs,
        }


def list_all_opportunities(analysis_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve opportunities, optionally filtered by analysis_id, with score and evidence count."""
    with Session(engine) as session:
        stmt = select(OpportunityDbRecord)
        if analysis_id:
            stmt = stmt.where(OpportunityDbRecord.strategic_analysis_id == analysis_id)
        stmt = stmt.limit(limit)
        opps = session.exec(stmt).all()

        scores_stmt = select(OpportunityScoreRecord)
        if analysis_id:
            scores_stmt = scores_stmt.where(OpportunityScoreRecord.strategic_analysis_id == analysis_id)
        scores = {s.opportunity_id: s.model_dump() for s in session.exec(scores_stmt).all()}

        results = []
        for opp in opps:
            opp_dict = opp.model_dump()
            score_data = scores.get(opp.opportunity_id)
            if score_data:
                opp_dict["raw_score"] = score_data.get("raw_score", 0.0)
                opp_dict["risk_adjusted_score"] = score_data.get("risk_adjusted_score", 0.0)
                opp_dict["component_scores"] = score_data.get("component_scores", {})
                opp_dict["scoring_rationale"] = score_data.get("scoring_rationale", {})
            results.append(opp_dict)

        results.sort(key=lambda x: x.get("risk_adjusted_score", 0.0), reverse=True)
        return results


def list_all_hypotheses(analysis_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve hypotheses, optionally filtered by analysis_id."""
    with Session(engine) as session:
        stmt = select(ResearchHypothesisRecord)
        if analysis_id:
            stmt = stmt.where(ResearchHypothesisRecord.strategic_analysis_id == analysis_id)
        stmt = stmt.limit(limit)
        return [h.model_dump() for h in session.exec(stmt).all()]


def list_all_risks(analysis_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve risks, optionally filtered by analysis_id."""
    with Session(engine) as session:
        stmt = select(RiskAssessmentRecord)
        if analysis_id:
            stmt = stmt.where(RiskAssessmentRecord.strategic_analysis_id == analysis_id)
        stmt = stmt.limit(limit)
        return [r.model_dump() for r in session.exec(stmt).all()]


def list_all_sources(research_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve sources, optionally filtered by research_id."""
    with Session(engine) as session:
        stmt = select(SourceDocumentRecord)
        if research_id:
            stmt = stmt.where(SourceDocumentRecord.research_id == research_id)
        stmt = stmt.order_by(desc(SourceDocumentRecord.created_at)).limit(limit)
        return [s.model_dump() for s in session.exec(stmt).all()]


def list_all_evidence(research_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve evidence records, optionally filtered by research_id."""
    with Session(engine) as session:
        stmt = select(EvidenceRecord)
        if research_id:
            stmt = stmt.where(EvidenceRecord.research_id == research_id)
        stmt = stmt.order_by(desc(EvidenceRecord.collected_at)).limit(limit)
        return [e.model_dump() for e in session.exec(stmt).all()]


def list_all_claims(research_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve claims, optionally filtered by research_id."""
    with Session(engine) as session:
        stmt = select(ResearchClaimRecord)
        if research_id:
            stmt = stmt.where(ResearchClaimRecord.research_id == research_id)
        stmt = stmt.limit(limit)
        return [c.model_dump() for c in session.exec(stmt).all()]


