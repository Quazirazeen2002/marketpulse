"""
Multi-Scenario Generator (Base, Best, Worst Case) for Opportunity Simulation.
"""

from typing import Dict, Any, Optional
from app.schemas.strategic import ScenarioInput, ScenarioResult, BusinessScenario
from app.services.business_simulation.calculator import calculate_scenario
from app.services.business_simulation.sensitivity import run_sensitivity_analysis


def build_scenario_suite(
    opportunity_id: str,
    opportunity_name: str,
    base_input: ScenarioInput,
) -> BusinessScenario:
    """
    Generate Base, Best, and Worst case outcomes along with sensitivity analysis.
    """
    # 1. Base Case
    base_res = calculate_scenario(base_input)

    # 2. Best Case (Optimistic: +20% volume, +10% price, -20% return rate, -15% delivery cost)
    best_input = base_input.model_copy(update={
        "scenario_name": "Best Case (Optimistic)",
        "expected_monthly_orders": int(round(base_input.expected_monthly_orders * 1.25)),
        "product_selling_price": round(base_input.product_selling_price * 1.08, 2),
        "return_refund_rate": max(0.01, round(base_input.return_refund_rate * 0.75, 3)),
        "delivery_cost_per_order": max(1.0, round(base_input.delivery_cost_per_order * 0.85, 2)),
    })
    best_res = calculate_scenario(best_input)

    # 3. Worst Case (Conservative: -25% volume, +30% return rate, +20% marketing, +15% delivery cost)
    worst_input = base_input.model_copy(update={
        "scenario_name": "Worst Case (Conservative)",
        "expected_monthly_orders": int(round(base_input.expected_monthly_orders * 0.75)),
        "return_refund_rate": min(0.35, round(base_input.return_refund_rate * 1.35, 3)),
        "monthly_marketing_expenditure": round(base_input.monthly_marketing_expenditure * 1.20, 2),
        "delivery_cost_per_order": round(base_input.delivery_cost_per_order * 1.15, 2),
    })
    worst_res = calculate_scenario(worst_input)

    # 4. Sensitivity
    sensitivity = run_sensitivity_analysis(base_input)

    notes = [
        "All calculations generated deterministically by Python financial arithmetic.",
        "Best Case assumes 25% higher monthly volume and 25% lower return rates via fit guidance.",
        "Worst Case factors 25% lower order volume and elevated return/marketing overhead.",
        "Simulated scenarios are illustrative models based on explicit user inputs and benchmarks.",
    ]

    return BusinessScenario(
        opportunity_id=opportunity_id,
        opportunity_name=opportunity_name,
        base_case=base_res,
        best_case=best_res,
        worst_case=worst_res,
        sensitivity=sensitivity,
        simulation_notes=notes,
    )


def generate_scenario_suite(
    base_input: ScenarioInput,
    opportunity_id: str = "custom-opp",
    opportunity_name: str = "Custom Opportunity",
) -> Dict[str, Any]:
    """Helper wrapper for API endpoints returning scenario cases dictionary."""
    scenario = build_scenario_suite(opportunity_id, opportunity_name, base_input)
    return {
        "base_case": scenario.base_case,
        "best_case": scenario.best_case,
        "worst_case": scenario.worst_case,
        "sensitivity": scenario.sensitivity,
        "simulation_notes": scenario.simulation_notes,
    }
