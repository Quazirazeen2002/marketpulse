import re
from typing import List, Optional
from app.schemas import SourceDocument, SourceQualityAssessment, SourceAcquisitionStatus
from .credibility import evaluate_publisher_credibility
from .freshness import evaluate_freshness
from .relevance import evaluate_relevance


def evaluate_source_quality(
    source: SourceDocument,
    objective: str,
    industry: str = "",
    geography: str = "",
    time_horizon: str = "Current",
) -> SourceQualityAssessment:
    """
    Compute transparent composite quality score (0-100) combining Credibility (25%),
    Relevance (25%), Freshness (15%), Completeness (20%), and Specificity (15%).
    """
    is_snippet = source.extraction_status == SourceAcquisitionStatus.SNIPPET_ONLY
    text = source.extracted_text or ""

    # 1. Credibility (25%)
    cred_score, cred_rat = evaluate_publisher_credibility(source.url, source.publisher)

    # 2. Relevance (25%)
    rel_score, rel_rat = evaluate_relevance(
        content=text,
        objective=objective,
        industry=industry,
        geography=geography,
    )

    # 3. Freshness (15%)
    is_time_sensitive = any(term in objective.lower() for term in ["price", "competitor", "campaign", "sale", "trend"])
    fresh_score, fresh_rat = evaluate_freshness(
        date_str=source.publication_date,
        time_horizon=time_horizon,
        is_pricing_or_campaign=is_time_sensitive,
    )

    # 4. Content Completeness (20%)
    if is_snippet:
        comp_score = 35.0
        comp_rat = "Snippet-only source; limited depth of empirical detail."
    elif len(text) > 4000:
        comp_score = 95.0
        comp_rat = f"Comprehensive full-text document ({len(text)} characters)."
    elif len(text) > 1500:
        comp_score = 80.0
        comp_rat = f"Adequate full-text document ({len(text)} characters)."
    elif len(text) > 500:
        comp_score = 65.0
        comp_rat = f"Partial document ({len(text)} characters)."
    else:
        comp_score = 40.0
        comp_rat = "Sparse text content."

    # 5. Evidence Specificity (15%)
    spec_matches = []
    # Metrics, numbers, percentages, currency
    num_matches = re.findall(r"\b\d+(?:\.\d+)?%|\b\d{4}\b|\b(?:BDT|USD|Tk|\$)\s*\d+", text)
    if num_matches:
        spec_score = min(95.0, 50.0 + len(num_matches) * 5.0)
        spec_matches.append(f"contains {len(num_matches)} quantitative data points")
    elif re.search(r"\b\d+\b", text):
        spec_score = 65.0
        spec_matches.append("contains numerical references")
    else:
        spec_score = 45.0
        spec_matches.append("largely qualitative narrative without statistical metrics")

    spec_rat = "; ".join(spec_matches)

    # Weighted composite score: 25% + 25% + 15% + 20% + 15%
    composite = (
        0.25 * cred_score +
        0.25 * rel_score +
        0.15 * fresh_score +
        0.20 * comp_score +
        0.15 * spec_score
    )
    composite = round(max(0.0, min(100.0, composite)), 1)

    rationale = (
        f"Composite Score: {composite}/100. "
        f"[Credibility: {cred_score:.0f}] {cred_rat} "
        f"[Relevance: {rel_score:.0f}] {rel_rat} "
        f"[Freshness: {fresh_score:.0f}] {fresh_rat} "
        f"[Completeness: {comp_score:.0f}] {comp_rat} "
        f"[Specificity: {spec_score:.0f}] {spec_rat}."
    )

    return SourceQualityAssessment(
        source_id=source.source_id,
        credibility_score=round(cred_score, 1),
        relevance_score=round(rel_score, 1),
        freshness_score=round(fresh_score, 1),
        completeness_score=round(comp_score, 1),
        specificity_score=round(spec_score, 1),
        composite_score=composite,
        scoring_rationale=rationale,
        is_snippet_only=is_snippet,
    )


class SourceQualityEvaluator:
    """Class wrapper for evaluating source quality across 5 dimensions."""

    def __init__(
        self,
        industry: str = "",
        geography: str = "",
        time_horizon: str = "Current",
    ):
        self.industry = industry
        self.geography = geography
        self.time_horizon = time_horizon

    def evaluate(
        self,
        source: SourceDocument,
        research_objective: str = "",
    ) -> SourceQualityAssessment:
        return evaluate_source_quality(
            source=source,
            objective=research_objective,
            industry=self.industry,
            geography=self.geography,
            time_horizon=self.time_horizon,
        )
