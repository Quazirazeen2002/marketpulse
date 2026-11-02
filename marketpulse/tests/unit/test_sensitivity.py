"""
Unit tests for 5-Dimensional Sensitivity Analysis.
Tests variations across Product Price, Order Volume, Marketing Spend, Delivery Cost, and Return Rate.
"""

import pytest
from app.services.business_simulation import run_sensitivity_analysis, ScenarioInput


def test_sensitivity_dimensions_coverage():
    """Verify 5 key dimensions are analyzed."""
    inp = ScenarioInput(
        product_selling_price=100.0,
        expected_monthly_orders=500,
        monthly_marketing_expenditure=5000.0,
        delivery_cost_per_order=5.0,
        return_refund_rate=0.05,
    )

    analyses = run_sensitivity_analysis(inp)
    assert len(analyses) == 5

    variables = {a.variable_tested for a in analyses}
    assert "Product Selling Price" in variables
    assert "Monthly Order Volume" in variables
    assert "Return/Refund Rate" in variables
    assert "Monthly Marketing Expenditure" in variables
    assert "Delivery Cost per Order" in variables


def test_sensitivity_directionality():
    """Verify that increasing price increases operating profit, and increasing return rate decreases profit."""
    inp = ScenarioInput(
        product_selling_price=100.0,
        expected_monthly_orders=500,
        monthly_marketing_expenditure=5000.0,
        delivery_cost_per_order=5.0,
        return_refund_rate=0.05,
        fixed_operating_expenses=8000.0,
    )

    analyses = run_sensitivity_analysis(inp)

    # Check Price sensitivity
    price_analysis = next(a for a in analyses if a.variable_tested == "Product Selling Price")
    assert len(price_analysis.variations) >= 2
    p_first = price_analysis.variations[0]
    p_last = price_analysis.variations[-1]
    assert p_last["monthly_operating_profit"] > p_first["monthly_operating_profit"]

    # Check Return Rate sensitivity
    return_analysis = next(a for a in analyses if a.variable_tested == "Return/Refund Rate")
    r_first = return_analysis.variations[0]
    r_last = return_analysis.variations[-1]
    # Lower return rate has higher profit than higher return rate
    assert r_first["monthly_operating_profit"] > r_last["monthly_operating_profit"]
