"""
Hypothesis Validator for Autonomous Opportunity Discovery.
Evaluates new evidence collected from follow-up investigations against hypotheses,
updating validation statuses and confidence levels.
"""

from typing import List, Dict, Any
from app.schemas.strategic import ResearchHypothesis, HypothesisStatus, utc_now_iso


from typing import List, Dict, Any, Union, Optional
from app.schemas.strategic import ResearchHypothesis, HypothesisStatus, utc_now_iso


def validate_hypotheses(
    hypotheses: Union[ResearchHypothesis, List[ResearchHypothesis]],
    new_evidence: Optional[List[Any]] = None,
    followup_results: Optional[List[Dict[str, Any]]] = None,
    contradictions: Optional[List[Any]] = None,
) -> Union[ResearchHypothesis, List[ResearchHypothesis]]:
    """
    Update hypothesis statuses based on newly retrieved empirical evidence and analyst reports.
    Supports single hypothesis or list of hypotheses.
    """
    is_single = isinstance(hypotheses, ResearchHypothesis)
    hyp_list = [hypotheses] if is_single else list(hypotheses)
    new_evidence = new_evidence or []
    followup_results = followup_results or []
    contradictions = contradictions or []

    new_ev_ids = []
    for e in new_evidence:
        if isinstance(e, dict) and e.get("evidence_id"):
            new_ev_ids.append(e.get("evidence_id"))
        elif isinstance(e, str):
            new_ev_ids.append(e)

    updated_hypotheses: List[ResearchHypothesis] = []

    for hyp in hyp_list:
        hyp_copy = hyp.model_copy()
        hyp_copy.updated_at = utc_now_iso()

        # Check if follow-up tasks were executed for this hypothesis
        matching_tasks = [t for t in followup_results if t.get("hypothesis_id") == hyp.hypothesis_id]

        task_ev = []
        for t in matching_tasks:
            task_ev.extend(t.get("new_evidence_ids", []))

        all_associated_ev = list(set(hyp_copy.evidence_ids + task_ev + new_ev_ids))
        hyp_copy.evidence_ids = all_associated_ev

        if contradictions:
            hyp_copy.contradicting_evidence.extend([str(c) for c in contradictions])
            if len(contradictions) >= len(all_associated_ev):
                hyp_copy.validation_status = HypothesisStatus.REJECTED
                hyp_copy.confidence_assessment = 0.20
                hyp_copy.final_disposition = "Refuted by contradictory evidence uncovered during follow-up investigation."
                updated_hypotheses.append(hyp_copy)
                continue

        if len(all_associated_ev) >= 2 or (new_ev_ids and not contradictions):
            hyp_copy.validation_status = HypothesisStatus.SUPPORTED
            hyp_copy.confidence_assessment = min(0.95, max(0.70, hyp_copy.confidence_assessment + 0.20))
            hyp_copy.final_disposition = (
                f"Validated by {len(all_associated_ev)} corroborating evidence records across targeted follow-up research."
            )
        elif len(all_associated_ev) == 1:
            hyp_copy.validation_status = HypothesisStatus.PARTIALLY_SUPPORTED
            hyp_copy.confidence_assessment = min(0.75, max(0.60, hyp_copy.confidence_assessment + 0.10))
            hyp_copy.final_disposition = "Partially supported by initial empirical evidence; requires further customer cohort validation."
        elif matching_tasks:
            hyp_copy.validation_status = HypothesisStatus.INCONCLUSIVE
            hyp_copy.confidence_assessment = max(0.40, hyp_copy.confidence_assessment - 0.10)
            hyp_copy.final_disposition = "Follow-up research yielded insufficient direct evidence to substantiate or refute."
        else:
            hyp_copy.validation_status = HypothesisStatus.INVESTIGATING

        updated_hypotheses.append(hyp_copy)

    return updated_hypotheses[0] if is_single else updated_hypotheses
