"""
AI Model Gateway for MARKETPULSE.
Enforces multi-model architecture:
- Research Director: Meta Muse Wonder (muse-wonder-1.0) for strategic planning & executive review.
- Specialist Agents: Spark 1.3 (spark-1.3) for rapid empirical synthesis across Market, Competitor, and Customer analysts.
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from app.config import settings


def get_director_model() -> Optional[ChatOpenAI]:
    """
    Model dedicated to Research Director.
    Uses Meta Muse Wonder (muse-wonder-1.0) for strategic reasoning,
    question decomposition, contradiction analysis, and executive synthesis.
    """
    if not (settings.META_API_KEY and settings.META_BASE_URL and settings.META_MUSE_WONDER_MODEL):
        return None

    return ChatOpenAI(
        model=settings.META_MUSE_WONDER_MODEL,
        api_key=settings.META_API_KEY,
        base_url=settings.META_BASE_URL,
        timeout=180,
        max_retries=2,
    )


class MetaSparkChatOpenAI(ChatOpenAI):
    """
    ChatOpenAI wrapper for Spark 1.3.
    Preserves model_name as 'spark-1.3' for strict role governance & test contracts,
    while mapping to the Meta API provider endpoint identifier 'muse-spark-1.3'.
    """
    def _get_request_payload(self, input_, *, stop=None, **kwargs):
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        if payload.get("model") in ("spark-1.3", "meta-spark-1.3") and "meta.ai" in str(self.openai_api_base):
            payload["model"] = "muse-spark-1.3"
        return payload


def get_specialist_model() -> Optional[ChatOpenAI]:
    """
    Model dedicated to all specialist research agents:
    - Market Intelligence Analyst
    - Competitor Intelligence Analyst
    - Customer Intelligence Analyst
    Uses Spark 1.3 (spark-1.3) for rapid, factual domain synthesis.
    """
    if not (settings.META_API_KEY and settings.META_BASE_URL and settings.META_SPARK_MODEL):
        return None

    return MetaSparkChatOpenAI(
        model=settings.META_SPARK_MODEL,
        api_key=settings.META_API_KEY,
        base_url=settings.META_BASE_URL,
        timeout=180,
        max_retries=2,
    )


# Permitted specialist roles mapped strictly to Spark 1.3
SPECIALIST_ROLES = {
    "market", "market_analyst", "market intelligence analyst",
    "competitor", "competitor_analyst", "competitor intelligence analyst",
    "customer", "customer_analyst", "customer intelligence analyst",
    "marketing", "marketing_analyst", "marketing intelligence analyst",
    "commercial", "commercial_analyst", "commercial intelligence analyst",
    "opportunity", "opportunity_analyst", "opportunity discovery analyst",
    "risk", "risk_analyst", "risk & industry intelligence analyst",
    "specialist",
}


def get_model_for_agent(agent_name: str) -> Optional[ChatOpenAI]:
    """
    Centralized Model Factory enforcing strict role allocation:
    - Research Director: Meta Muse Wonder (muse-wonder-1.0)
    - All 7 Specialists: Meta Spark 1.3 (spark-1.3)
    Never silently switches models.
    """
    role = agent_name.lower().strip()
    if "director" in role:
        return get_director_model()
    return get_specialist_model()


def get_research_model(agent_role: str = "director") -> Optional[ChatOpenAI]:
    """Router returning the designated model for a given agent role."""
    return get_model_for_agent(agent_role)


def director_model_available() -> bool:
    """Check if Muse Wonder is configured for Research Director."""
    return get_director_model() is not None


def specialist_model_available() -> bool:
    """Check if Spark 1.3 is configured for Specialist Analysts."""
    return get_specialist_model() is not None


def model_available() -> bool:
    """Check if research models are configured."""
    return director_model_available() or specialist_model_available()
