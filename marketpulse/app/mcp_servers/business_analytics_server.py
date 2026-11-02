"""
Business Analytics MCP Server for MARKETPULSE Stage 2.
Exposes deterministic financial arithmetic tools for unit economics,
break-even analysis, contribution margins, and scenario comparisons.
"""

from typing import Dict, Any, List, Optional
from app.mcp_servers.base import MCPServer
from app.schemas.strategic import ScenarioInput
from app.services.business_simulation.calculator import calculate_scenario
from app.services.business_simulation.break_even import calculate_break_even_metrics
from app.services.business_simulation.sensitivity import run_sensitivity_analysis as run_sens_calc

analytics_server = MCPServer(name="business_analytics", version="1.0.0")


def calculate_unit_economics(
    selling_price: float,
    product_cost: Optional[float] = None,
    cogs: Optional[float] = None,
    delivery_cost: float = 0.0,
    payment_fee: float = 0.0,
    payment_fee_pct: float = 0.0,
    other_variable: float = 0.0,
    **kwargs,
) -> Dict[str, Any]:
    """Calculate deterministic unit gross and contribution margin."""
    cost = product_cost if product_cost is not None else (cogs if cogs is not None else 0.0)
    gross_profit = selling_price - cost
    gross_margin_pct = (gross_profit / selling_price * 100.0) if selling_price > 0 else 0.0
    fee = payment_fee if payment_fee > 0 else (selling_price * payment_fee_pct)
    unit_contribution = gross_profit - delivery_cost - fee - other_variable
    contribution_margin_pct = (unit_contribution / selling_price * 100.0) if selling_price > 0 else 0.0

    return {
        "selling_price": round(selling_price, 2),
        "product_cost": round(cost, 2),
        "cogs": round(cost, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_percent": round(gross_margin_pct, 1),
        "contribution_margin": round(unit_contribution, 2),
        "unit_contribution": round(unit_contribution, 2),
        "contribution_margin_percent": round(contribution_margin_pct, 1),
        "is_positive_contribution": unit_contribution > 0,
    }


def calculate_break_even(
    selling_price: float,
    product_cost: float,
    fixed_costs: float,
    variable_costs_per_unit: float = 5.0,
) -> Dict[str, Any]:
    """Calculate break-even units and revenue deterministically."""
    return calculate_break_even_metrics(
        selling_price=selling_price,
        unit_cost=product_cost,
        variable_cost_per_order=variable_costs_per_unit,
        fixed_costs=fixed_costs,
    )


def compare_scenarios(scenario_a: Dict[str, Any], scenario_b: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two financial scenario outcomes."""
    inp_a = ScenarioInput(**scenario_a)
    inp_b = ScenarioInput(**scenario_b)
    res_a = calculate_scenario(inp_a)
    res_b = calculate_scenario(inp_b)

    profit_diff = res_b.monthly_operating_profit - res_a.monthly_operating_profit
    return {
        "scenario_a_profit": res_a.monthly_operating_profit,
        "scenario_b_profit": res_b.monthly_operating_profit,
        "difference": round(profit_diff, 2),
        "higher_performing": res_b.scenario_name if profit_diff > 0 else res_a.scenario_name,
    }


def calculate_contribution_margin(revenue: float, variable_costs: float) -> Dict[str, Any]:
    """Calculate aggregate contribution margin dollars and percentage."""
    cm_dollars = revenue - variable_costs
    cm_pct = (cm_dollars / revenue * 100.0) if revenue > 0 else 0.0
    return {
        "revenue": round(revenue, 2),
        "variable_costs": round(variable_costs, 2),
        "contribution_margin_dollars": round(cm_dollars, 2),
        "contribution_margin_percent": round(cm_pct, 1),
    }


def run_sensitivity(
    selling_price: float,
    product_cost: float,
    monthly_orders: int,
    fixed_expenses: float,
    marketing_expenditure: float,
) -> Dict[str, Any]:
    """Run sensitivity permutations on a baseline scenario."""
    base_inp = ScenarioInput(
        product_selling_price=selling_price,
        product_cost=product_cost,
        expected_monthly_orders=monthly_orders,
        fixed_operating_expenses=fixed_expenses,
        monthly_marketing_expenditure=marketing_expenditure,
    )
    sens_list = run_sens_calc(base_inp)
    return {"sensitivity_results": [s.model_dump() for s in sens_list]}


# Register tools
analytics_server.register_tool(
    name="calculate_unit_economics",
    description="Calculate gross margin, variable costs, and contribution margin per unit.",
    input_schema={
        "type": "object",
        "properties": {
            "selling_price": {"type": "number", "description": "Product retail price"},
            "product_cost": {"type": "number", "description": "Product acquisition cost"},
            "delivery_cost": {"type": "number", "description": "Delivery cost per order", "default": 5.0},
        },
        "required": ["selling_price", "product_cost"],
    },
    func=calculate_unit_economics,
)

analytics_server.register_tool(
    name="calculate_break_even",
    description="Calculate break-even order volume and break-even revenue.",
    input_schema={
        "type": "object",
        "properties": {
            "selling_price": {"type": "number"},
            "product_cost": {"type": "number"},
            "fixed_costs": {"type": "number"},
            "variable_costs_per_unit": {"type": "number", "default": 5.0},
        },
        "required": ["selling_price", "product_cost", "fixed_costs"],
    },
    func=calculate_break_even,
)

analytics_server.register_tool(
    name="calculate_contribution_margin",
    description="Calculate contribution margin in currency and percentage.",
    input_schema={
        "type": "object",
        "properties": {
            "revenue": {"type": "number"},
            "variable_costs": {"type": "number"},
        },
        "required": ["revenue", "variable_costs"],
    },
    func=calculate_contribution_margin,
)
