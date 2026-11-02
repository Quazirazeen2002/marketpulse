"""
LangGraph Workflow Builder for MARKETPULSE Stage 1.
Assembles the complete state graph with validation, decomposition,
parallel specialist research branches, cross-agent synthesis & claim verification,
director executive review, conditional routing, and persistence.
"""

from langgraph.graph import StateGraph, START, END
from app.graph.state import MarketPulseState
from app.graph.nodes import (
    validate_request_node,
    decompose_questions_node,
    market_analyst_node,
    competitor_analyst_node,
    customer_analyst_node,
    cross_agent_synthesis_node,
    director_review_node,
    persist_results_node,
)


def route_after_validation(state: MarketPulseState) -> str:
    """Conditional router: abort if validation fails; otherwise decompose questions."""
    if state.get("research_status") == "failed" or state.get("errors"):
        return "persist_results"
    return "decompose_questions"


def route_after_synthesis(state: MarketPulseState) -> str:
    """
    Conditional router: if contradictions are present or evidence is thin,
    ensure director executes with specialized awareness.
    """
    # Always routes to director_review for full synthesis
    return "director_review"


def build_graph():
    """Construct and compile the production LangGraph research workflow."""
    builder = StateGraph(MarketPulseState)

    # 1. Add all core workflow nodes
    builder.add_node("validate_request", validate_request_node)
    builder.add_node("decompose_questions", decompose_questions_node)
    builder.add_node("market_analyst", market_analyst_node)
    builder.add_node("competitor_analyst", competitor_analyst_node)
    builder.add_node("customer_analyst", customer_analyst_node)
    builder.add_node("cross_agent_synthesis", cross_agent_synthesis_node)
    builder.add_node("director_review", director_review_node)
    builder.add_node("persist_results", persist_results_node)

    # 2. Add edges and conditional routing
    builder.add_edge(START, "validate_request")

    builder.add_conditional_edges(
        "validate_request",
        route_after_validation,
        {
            "decompose_questions": "decompose_questions",
            "persist_results": "persist_results",
        },
    )

    # Parallel branch execution for the three specialist analysts
    builder.add_edge("decompose_questions", "market_analyst")
    builder.add_edge("decompose_questions", "competitor_analyst")
    builder.add_edge("decompose_questions", "customer_analyst")

    # Specialists join into cross-agent synthesis
    builder.add_edge(
        ["market_analyst", "competitor_analyst", "customer_analyst"],
        "cross_agent_synthesis",
    )

    builder.add_conditional_edges(
        "cross_agent_synthesis",
        route_after_synthesis,
        {
            "director_review": "director_review",
        },
    )

    builder.add_edge("director_review", "persist_results")
    builder.add_edge("persist_results", END)

    return builder.compile()


# Compile global workflow graph instance
marketpulse_graph = build_graph()
