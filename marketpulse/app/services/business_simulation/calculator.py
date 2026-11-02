"""
Deterministic Financial Calculator for Business Scenario Simulation.
Authoritative Python financial arithmetic for unit economics, contribution margins,
and operating profitability.
"""

import math
from app.schemas.strategic import ScenarioInput, ScenarioResult
from app.services.business_simulation.validation import validate_scenario_input


def calculate_scenario(inp: ScenarioInput) -> ScenarioResult:
    """
    Perform deterministic financial calculation for a single business scenario.
    """
    is_valid, errors = validate_scenario_input(inp)
    if not is_valid:
        raise ValueError(f"Invalid scenario input parameters: {'; '.join(errors)}")

    # 1. Volume & Revenue
    effective_orders = inp.expected_monthly_orders * (1.0 - inp.return_refund_rate)
    monthly_revenue = effective_orders * inp.product_selling_price

    # 2. Cost of Goods Sold (COGS)
    cogs = effective_orders * inp.product_cost
    gross_profit = monthly_revenue - cogs
    gross_margin_pct = (gross_profit / monthly_revenue * 100.0) if monthly_revenue > 0 else 0.0

    # 3. Variable Operating Costs
    delivery_costs = inp.expected_monthly_orders * inp.delivery_cost_per_order
    processing_fees = monthly_revenue * inp.payment_processing_fee_percent
    other_variable = effective_orders * inp.other_variable_cost_per_order
    variable_operating_costs = delivery_costs + processing_fees + other_variable

    # 4. Contribution Margin
    net_contribution = gross_profit - variable_operating_costs
    contribution_per_order = (net_contribution / effective_orders) if effective_orders > 0 else 0.0
    contribution_margin_pct = (net_contribution / monthly_revenue * 100.0) if monthly_revenue > 0 else 0.0

    # 5. Fixed Operating Costs
    fixed_operating_costs = inp.fixed_operating_expenses + inp.monthly_marketing_expenditure
    total_operating_costs = cogs + variable_operating_costs + fixed_operating_costs

    # 6. Operating Profit
    monthly_operating_profit = monthly_revenue - total_operating_costs
    annual_operating_profit = monthly_operating_profit * 12.0

    # 7. Break-Even Calculations
    if contribution_per_order > 0:
        break_even_orders = int(math.ceil(fixed_operating_costs / contribution_per_order))
        break_even_revenue = round(break_even_orders * inp.product_selling_price, 2)
    else:
        break_even_orders = 999999
        break_even_revenue = 99999999.0

    # 8. Estimated Cash Requirement (Initial capital + 3-month operating loss buffer if unprofitable)
    cash_buffer = abs(monthly_operating_profit) * 3.0 if monthly_operating_profit < 0 else 0.0
    estimated_cash = round(inp.initial_investment + cash_buffer, 2)

    return ScenarioResult(
        scenario_name=inp.scenario_name,
        monthly_revenue=round(monthly_revenue, 2),
        cogs=round(cogs, 2),
        gross_profit=round(gross_profit, 2),
        gross_margin_percent=round(gross_margin_pct, 1),
        contribution_per_order=round(contribution_per_order, 2),
        contribution_margin_percent=round(contribution_margin_pct, 1),
        variable_operating_costs=round(variable_operating_costs, 2),
        fixed_operating_costs=round(fixed_operating_costs, 2),
        total_operating_costs=round(total_operating_costs, 2),
        monthly_operating_profit=round(monthly_operating_profit, 2),
        annual_operating_profit=round(annual_operating_profit, 2),
        break_even_orders=break_even_orders,
        break_even_revenue=break_even_revenue,
        estimated_cash_requirement=estimated_cash,
        is_profitable=(monthly_operating_profit > 0),
    )
