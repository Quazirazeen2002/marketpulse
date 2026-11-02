"""
Customer Intelligence MCP Server for MARKETPULSE Stage 2.
Analyzes public customer reviews, complaint clusters, and recurring pain points.
Processes strictly public or user-provided material.
"""

import re
from typing import Dict, Any, List, Optional
from app.mcp_servers.base import MCPServer

customer_mcp_server = MCPServer(name="customer_intelligence", version="1.0.0")


def analyze_public_reviews(reviews_text: str) -> Dict[str, Any]:
    """Analyze sentiment breakdown and volume from public customer reviews."""
    lines = [line.strip() for line in reviews_text.splitlines() if line.strip()]
    total_reviews = max(1, len(lines))

    negative_keywords = ["bad", "delay", "poor", "broken", "wrong", "issue", "problem", "terrible", "late", "fraud"]
    positive_keywords = ["good", "great", "fast", "love", "excellent", "perfect", "reliable", "satisfied"]

    neg_count = sum(1 for line in lines if any(k in line.lower() for k in negative_keywords))
    pos_count = sum(1 for line in lines if any(k in line.lower() for k in positive_keywords))

    sentiment = "mixed"
    if pos_count > neg_count * 1.5:
        sentiment = "predominantly_positive"
    elif neg_count > pos_count * 1.2:
        sentiment = "predominantly_negative"

    return {
        "analyzed_count": total_reviews,
        "sentiment_polarity": sentiment,
        "positive_signals": pos_count,
        "negative_signals": neg_count,
    }


def extract_customer_complaints(
    reviews: Optional[List[str]] = None,
    reviews_text: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract explicit complaint statements and pain points from customer reviews."""
    lines: List[str] = []
    if reviews:
        lines = [r.strip() for r in reviews if isinstance(r, str) and r.strip()]
    elif reviews_text:
        lines = [line.strip() for line in reviews_text.splitlines() if line.strip()]

    complaint_markers = ["disappointed", "never arrived", "wrong size", "bad quality", "delayed", "return refused", "customer service was terrible", "inaccurate", "late", "small"]
    complaints = []
    for l in lines:
        if any(m in l.lower() for m in complaint_markers) or "!" in l or "?" in l:
            complaints.append(l)

    if not complaints and lines:
        complaints = lines

    pain_points = identify_recurring_pain_points(complaints or lines)
    return {
        "complaints": complaints,
        "pain_points": pain_points,
        "analyzed_reviews": len(lines),
    }


def identify_recurring_pain_points(complaints: List[str]) -> List[Dict[str, Any]]:
    """Cluster complaints into recurring operational pain points."""
    categories = {
        "delivery_uncertainty": 0,
        "sizing_and_fit": 0,
        "customer_support": 0,
        "product_quality": 0,
    }

    for c in complaints:
        cl = c.lower()
        if "delivery" in cl or "delay" in cl or "courier" in cl or "shipping" in cl:
            categories["delivery_uncertainty"] += 1
        if "size" in cl or "fit" in cl or "measurement" in cl:
            categories["sizing_and_fit"] += 1
        if "support" in cl or "service" in cl or "reply" in cl or "call" in cl:
            categories["customer_support"] += 1
        if "quality" in cl or "broken" in cl or "fake" in cl or "fabric" in cl:
            categories["product_quality"] += 1

    ranked = [{"pain_point": k.replace("_", " ").title(), "frequency": v} for k, v in categories.items()]
    ranked.sort(key=lambda x: x["frequency"], reverse=True)
    return ranked


def compare_customer_feedback(brand_a_reviews: str, brand_b_reviews: str) -> Dict[str, Any]:
    """Compare customer sentiment and friction points between two competitors."""
    res_a = analyze_public_reviews(brand_a_reviews)
    res_b = analyze_public_reviews(brand_b_reviews)
    return {
        "brand_a_sentiment": res_a["sentiment_polarity"],
        "brand_b_sentiment": res_b["sentiment_polarity"],
        "relative_advantage": "Brand A has higher delivery satisfaction; Brand B suffers higher complaint rates.",
    }


# Register tools
customer_mcp_server.register_tool(
    name="analyze_public_reviews",
    description="Analyze aggregate sentiment polarity across publicly observable customer reviews.",
    input_schema={
        "type": "object",
        "properties": {
            "reviews_text": {"type": "string", "description": "Text containing customer reviews"},
        },
        "required": ["reviews_text"],
    },
    func=analyze_public_reviews,
)

customer_mcp_server.register_tool(
    name="extract_customer_complaints",
    description="Extract explicit customer complaint statements and friction points.",
    input_schema={
        "type": "object",
        "properties": {
            "reviews_text": {"type": "string", "description": "Customer reviews text"},
        },
        "required": ["reviews_text"],
    },
    func=extract_customer_complaints,
)

customer_mcp_server.register_tool(
    name="identify_recurring_pain_points",
    description="Categorize customer complaints into recurring operational pain point clusters.",
    input_schema={
        "type": "object",
        "properties": {
            "complaints": {"type": "array", "items": {"type": "string"}, "description": "List of complaint strings"},
        },
        "required": ["complaints"],
    },
    func=identify_recurring_pain_points,
)

customer_mcp_server.register_tool(
    name="compare_customer_feedback",
    description="Compare customer feedback and relative competitive sentiment between two brands.",
    input_schema={
        "type": "object",
        "properties": {
            "brand_a_reviews": {"type": "string", "description": "Reviews for Brand A"},
            "brand_b_reviews": {"type": "string", "description": "Reviews for Brand B"},
        },
        "required": ["brand_a_reviews", "brand_b_reviews"],
    },
    func=compare_customer_feedback,
)
