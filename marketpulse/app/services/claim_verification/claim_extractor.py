import re
import uuid
from typing import List, Optional
from app.schemas import ResearchClaim, ClaimType, ClaimStatus


def extract_atomic_claims(
    analysis_text: str,
    agent_name: str,
    evidence_ids: List[str] = None,
    max_claims: int = 6,
) -> List[ResearchClaim]:
    """
    Extract discrete, atomic testable claims from analytical prose.
    Classifies claim types and flags speculative statements as hypotheses.
    """
    if not analysis_text:
        return []

    evidence_ids = evidence_ids or []
    claims: List[ResearchClaim] = []

    # Split into candidate sentences or bullet lines
    lines = [
        line.strip().lstrip("-*•0123456789. ")
        for line in analysis_text.split("\n")
        if len(line.strip().lstrip("-*•0123456789. ")) > 35
    ]

    # If few lines, split by sentences
    if len(lines) < 2:
        lines = [s.strip() for s in re.split(r"(?<=[.!?])\s+", analysis_text) if len(s.strip()) > 35]

    for idx, sentence in enumerate(lines[:max_claims], 1):
        # Skip pure introductory or meta statements
        if any(skip in sentence.lower() for skip in ["i have analyzed", "in conclusion", "here is the summary", "as an ai"]):
            continue

        claim_id = f"CLM-{uuid.uuid4().hex[:6].upper()}"
        lower_s = sentence.lower()

        # Detect hypothesis / speculative language
        is_hypo = any(h in lower_s for h in ["might", "could", "may", "potentially", "likely", "hypothesize", "suggests that"])

        # Determine Claim Type
        if any(term in lower_s for term in ["competitor", "daraz", "aarong", "fabrilife", "pricing", "discount", "campaign"]):
            ctype = ClaimType.COMPETITOR_STRATEGY
        elif any(term in lower_s for term in ["customer", "consumer", "buyer", "complaint", "review", "preference"]):
            ctype = ClaimType.CUSTOMER_BEHAVIOR
        elif any(term in lower_s for term in ["market size", "cagr", "growth", "segment", "industry", "market share"]):
            ctype = ClaimType.MARKET_STRUCTURE
        elif any(term in lower_s for term in ["opportunity", "gap", "underserved", "niche", "potential"]):
            ctype = ClaimType.COMMERCIAL_OPPORTUNITY
        elif is_hypo:
            ctype = ClaimType.HYPOTHESIS
        else:
            ctype = ClaimType.FACT

        claims.append(
            ResearchClaim(
                claim_id=claim_id,
                agent_name=agent_name,
                claim_text=sentence,
                claim_type=ctype,
                supporting_evidence_ids=evidence_ids[:3],
                verification_status=ClaimStatus.UNVERIFIED,
                confidence_score=0.5 if not is_hypo else 0.35,
                verification_rationale="Initial extraction pending cross-source verification.",
                is_hypothesis=is_hypo,
            )
        )

    return claims


class ClaimExtractor:
    """Class wrapper for extracting atomic claims from analytical text."""

    def __init__(self, max_claims: int = 6):
        self.max_claims = max_claims

    def extract_claims(
        self,
        text: str,
        agent_name: str,
        available_evidence_ids: Optional[List[str]] = None,
    ) -> List[ResearchClaim]:
        return extract_atomic_claims(
            analysis_text=text,
            agent_name=agent_name,
            evidence_ids=available_evidence_ids or [],
            max_claims=self.max_claims,
        )
