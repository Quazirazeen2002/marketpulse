"""
Unit tests for Deterministic Financial Calculator and Break-Even Engine.
Uses known mathematical ground truth test cases.
Never relies on LLM arithmetic.
"""

import pytest
from app.services.business_simulation import (
    calculate_scenario,
    calculate_break_even_metrics,
    validate_scenario_input,
    ScenarioInput,
)


def test_deterministic_scenario_calculation_known_case():
    """
    Known Mathematical Benchmark Test:
    - Selling Price = $100.00
    - Product Cost (COGS) = $40.00
    - Monthly Orders = 500
    - Delivery Cost = $5.00
    - Return Rate = 5% (0.05)
    - Payment Gateway Fee = 2.5% (0.025 * 100 = $2.50)
    - Other Variable Cost = $2.00
    - Monthly Marketing = $5,000.00
    - Fixed Overheads = $8,000.00
    """
    inp = ScenarioInput(
        scenario_name="Benchmark Case",
        initial_investment=50000.0,
        product_selling_price=100.0,
        product_cost=40.0,
        expected_monthly_orders=500,
        monthly_marketing_expenditure=5000.0,
        delivery_cost_per_order=5.0,
        return_refund_rate=0.05,
        fixed_operating_expenses=8000.0,
        payment_processing_fee_percent=0.025,
        other_variable_cost_per_order=2.0,
    )

    result = calculate_scenario(inp)

    # 1. Net Revenue after 5% refunds = $50,000 * 0.95 = $47,500
    assert result.monthly_revenue == 47500.0

    # 2. COGS for delivered items = 500 * $40 * 0.95 = $19,000
    # Gross Profit = $47,500 - $19,000 = $28,500
    assert result.cogs == 19000.0
    assert result.gross_profit == 28500.0
    assert result.gross_margin_percent == 60.0

    # 3. Variable operating costs per order:
    assert result.contribution_per_order > 0
    assert result.contribution_margin_percent > 0

    # 4. Total fixed overheads = Marketing ($5,000) + Fixed ($8,000) = $13,000
    assert result.fixed_operating_costs == 13000.0

    # 5. Break-even volume
    assert result.break_even_orders > 0
    assert result.break_even_revenue > 0

    # 6. Monthly operating profit & Profitability
    assert result.annual_operating_profit == result.monthly_operating_profit * 12


def test_input_validation_boundaries():
    """Verify validation rejects impossible or negative values."""
    with pytest.raises(Exception):
        validate_scenario_input(product_selling_price=-10.0)

    with pytest.raises(Exception):
        validate_scenario_input(return_refund_rate=1.5)  # cannot be > 100%

    with pytest.raises(Exception):
        validate_scenario_input(expected_monthly_orders=-50)


def test_break_even_edge_cases():
    """Verify break-even calculation handles negative or zero contribution gracefully."""
    # When variable cost exceeds price, contribution <= 0 -> status is unviable_unit_economics
    metrics = calculate_break_even_metrics(
        selling_price=50.0,
        unit_cost=30.0,
        variable_cost_per_order=30.0,  # Total variable = 60 > 50
        fixed_costs=10000.0,
    )
    assert metrics["break_even_units"] == -1
    assert metrics["status"] == "unviable_unit_economics"
