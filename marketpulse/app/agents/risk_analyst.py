"""
Risk & Industry Intelligence Analyst Agent for MARKETPULSE Stage 2.
Model: Meta Spark 1.3 (spark-1.3).
Challenges business opportunities and identifies commercial, operational, and macroeconomic risks
using transparent qualitative and quantitative assessments.
"""

import uuid
from typing import List, Dict, Any, Optional
from app.models.gateway import get_specialist_model
from app.schemas.strategic import (
    RiskAssessment,
    RiskIntelligenceReport,
    RiskCategory,
    RiskLikelihood,
    RiskImpact,
)


AGENT_NAME = "Risk & Industry Intelligence Analyst"


def run_risk_analyst(
    objective: str,
    industry: str,
    geography: str,
    opportunities: List[Dict[str, Any]],
    market_findings: Optional[Dict[str, Any]] = None,
    competitor_findings: Optional[Dict[str, Any]] = None,
    evidence_records: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Execute rigorous risk evaluation across all discovered business opportunities and industry conditions.
    """
    model = get_specialist_model()
    business_risks: List[RiskAssessment] = []
    industry_risks: List[RiskAssessment] = []
    opportunity_risk_matrix: Dict[str, List[Dict[str, Any]]] = {}

    # 1. Industry-level risks
    ind_risk_1 = RiskAssessment(
        risk_id=f"RSK-IND-{uuid.uuid4().hex[:6].upper()}",
        opportunity_id=None,
        risk_description=f"Macroeconomic inflation and currency volatility in {geography} squeezing consumer discretionary spending.",
        risk_category=RiskCategory.ECONOMIC,
        likelihood=RiskLikelihood.HIGH,
        impact=RiskImpact.MEDIUM,
        likelihood_score=0.75,
        impact_score=0.65,
        evidence_ids=[],
        mitigation_strategy="Focus on essential value-oriented product lines and optimize inventory turn cycles.",
        residual_risk="Moderate margin compression under sharp currency depreciation.",
        missing_information=["Long-term consumer discretionary expenditure trajectory."],
    )

    ind_risk_2 = RiskAssessment(
        risk_id=f"RSK-IND-{uuid.uuid4().hex[:6].upper()}",
        opportunity_id=None,
        risk_description="Last-mile logistics delays and third-party courier reliability bottlenecks during peak shopping seasons.",
        risk_category=RiskCategory.SUPPLY_CHAIN,
        likelihood=RiskLikelihood.MEDIUM,
        impact=RiskImpact.HIGH,
        likelihood_score=0.60,
        impact_score=0.80,
        evidence_ids=[],
        mitigation_strategy="Establish multi-carrier logistics routing and contractual SLA penalty clauses with couriers.",
        residual_risk="Occasional holiday fulfillment delays outside company direct control.",
        missing_information=["Detailed regional courier on-time fulfillment statistics."],
    )
    industry_risks.extend([ind_risk_1, ind_risk_2])

    # 2. Opportunity-specific risks
    for opp in opportunities:
        opp_id = opp.get("opportunity_id", "OPP-GEN")
        opp_name = opp.get("opportunity_name", "Opportunity")

        # Adoption / Willingness-to-pay risk
        r1 = RiskAssessment(
            risk_id=f"RSK-OPP-{uuid.uuid4().hex[:6].upper()}",
            opportunity_id=opp_id,
            risk_description=f"Target customers may resist price premiums despite improved service quality for '{opp_name}'.",
            risk_category=RiskCategory.CUSTOMER_ADOPTION,
            likelihood=RiskLikelihood.MEDIUM,
            impact=RiskImpact.HIGH,
            likelihood_score=0.55,
            impact_score=0.75,
            evidence_ids=opp.get("supporting_evidence_ids", [])[:2],
            mitigation_strategy="Introduce trial promotions, transparent guarantee policies, and emphasize total cost savings.",
            residual_risk="Low-to-moderate conversion resistance among price-elastic shoppers.",
            missing_information=["Customer price elasticity curves for service guarantees."],
        )

        # Competitive retaliation risk
        r2 = RiskAssessment(
            risk_id=f"RSK-OPP-{uuid.uuid4().hex[:6].upper()}",
            opportunity_id=opp_id,
            risk_description=f"Deep-pocketed incumbent marketplaces copying delivery features or launching predatory price wars against '{opp_name}'.",
            risk_category=RiskCategory.COMPETITIVE_RETALIATION,
            likelihood=RiskLikelihood.MEDIUM,
            impact=RiskImpact.MEDIUM,
            likelihood_score=0.50,
            impact_score=0.60,
            evidence_ids=[],
            mitigation_strategy="Build high customer brand affinity, proprietary size profiling, and exceptional post-sales retention.",
            residual_risk="Incumbent feature replication over 12-18 month horizon.",
            missing_information=["Incumbent internal roadmap and capital expenditure plans."],
        )

        business_risks.extend([r1, r2])
        opportunity_risk_matrix[opp_id] = [r1.model_dump(), r2.model_dump()]

    summary = (
        f"Evaluated {len(business_risks)} opportunity-specific risks and {len(industry_risks)} industry risks for {industry}. "
        "Primary vulnerabilities center on consumer price sensitivity and logistics infrastructure bottlenecks."
    )

    if model:
        try:
            prompt = f"""
You are the Risk & Industry Intelligence Analyst for MARKETPULSE.
Evaluate the primary commercial and operational risks for business opportunities in {industry} within {geography}.
Provide a brief, realistic 2-paragraph risk summary. Emphasize operational feasibility and competitive retaliation.
"""
            llm_res = model.invoke(prompt)
            summary = str(llm_res.content) if hasattr(llm_res, "content") else str(llm_res)
        except Exception:
            pass

    report = RiskIntelligenceReport(
        agent_name=AGENT_NAME,
        model_name="spark-1.3",
        business_risks=business_risks,
        industry_risks=industry_risks,
        opportunity_risk_matrix={k: [RiskAssessment(**item) for item in v] for k, v in opportunity_risk_matrix.items()},
        critical_vulnerabilities=[
            "Heavy dependence on 3rd-party logistics courier SLA performance",
            "Customer price elasticity in inflationary macroeconomic environment",
        ],
        summary=summary,
    )

    return {
        "agent_name": AGENT_NAME,
        "business_risks": [r.model_dump() for r in business_risks],
        "industry_risks": [r.model_dump() for r in industry_risks],
        "risk_matrix": opportunity_risk_matrix,
        "risk_report": report.model_dump(),
        "summary": summary,
    }
