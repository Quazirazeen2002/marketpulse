"""
Strategic LangGraph Workflow Definition for MARKETPULSE Stage 2.
Constructs StateGraph with conditional autonomous exploration loops and deterministic persistence.
"""

from langgraph.graph import StateGraph, START, END

from app.graph.strategic_state import StrategicState
from app.graph.strategic_nodes import (
    load_stage1_research_node,
    strategic_planning_node,
    parallel_specialists_node,
    strategic_synthesis_node,
    followup_investigation_node,
    opportunity_scoring_node,
    scenario_simulation_node,
    strategic_executive_report_node,
    persist_strategic_analysis_node,
)
from app.graph.strategic_routing import should_execute_followup


def create_strategic_graph():
    """Build and compile the Stage 2 Strategic Intelligence LangGraph workflow."""
    workflow = StateGraph(StrategicState)

    # Register Nodes
    workflow.add_node("load_stage1_research", load_stage1_research_node)
    workflow.add_node("strategic_planning", strategic_planning_node)
    workflow.add_node("parallel_specialists", parallel_specialists_node)
    workflow.add_node("strategic_synthesis", strategic_synthesis_node)
    workflow.add_node("followup_investigation", followup_investigation_node)
    workflow.add_node("opportunity_scoring", opportunity_scoring_node)
    workflow.add_node("scenario_simulation", scenario_simulation_node)
    workflow.add_node("strategic_executive_report", strategic_executive_report_node)
    workflow.add_node("persist_strategic_analysis", persist_strategic_analysis_node)

    # Connect Edges
    workflow.add_edge(START, "load_stage1_research")
    workflow.add_edge("load_stage1_research", "strategic_planning")
    workflow.add_edge("strategic_planning", "parallel_specialists")
    workflow.add_edge("parallel_specialists", "strategic_synthesis")

    # Conditional Routing for Autonomous Follow-up Research
    workflow.add_conditional_edges(
        "strategic_synthesis",
        should_execute_followup,
        {
            "followup_investigation": "followup_investigation",
            "opportunity_scoring": "opportunity_scoring",
        },
    )

    workflow.add_edge("followup_investigation", "opportunity_scoring")
    workflow.add_edge("opportunity_scoring", "scenario_simulation")
    workflow.add_edge("scenario_simulation", "strategic_executive_report")
    workflow.add_edge("strategic_executive_report", "persist_strategic_analysis")
    workflow.add_edge("persist_strategic_analysis", END)

    return workflow.compile()


# Singleton compiled graph instance
strategic_graph = create_strategic_graph()
