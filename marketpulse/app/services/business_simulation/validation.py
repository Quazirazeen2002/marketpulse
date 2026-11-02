"""
Input Validation for Business Scenario Simulator.
Prevents impossible arithmetic, negative costs, or zero-division crashes.
"""

from typing import List, Tuple
from app.schemas.strategic import ScenarioInput


def validate_scenario_input(inp: ScenarioInput) -> Tuple[bool, List[str]]:
    """Validate scenario assumptions for mathematical and commercial validity."""
    errors = []

    if inp.product_selling_price <= 0:
        errors.append("Product selling price must be greater than zero.")
    if inp.product_cost < 0:
        errors.append("Product cost cannot be negative.")
    if inp.product_cost >= inp.product_selling_price:
        errors.append("Product cost exceeds or equals selling price; unit economics are inherently negative.")
    if inp.expected_monthly_orders < 0:
        errors.append("Expected monthly orders cannot be negative.")
    if inp.monthly_marketing_expenditure < 0:
        errors.append("Monthly marketing expenditure cannot be negative.")
    if inp.delivery_cost_per_order < 0:
        errors.append("Delivery cost per order cannot be negative.")
    if not (0.0 <= inp.return_refund_rate < 1.0):
        errors.append("Return/refund rate must be between 0.0 and 0.99.")
    if inp.fixed_operating_expenses < 0:
        errors.append("Fixed operating expenses cannot be negative.")
    if not (0.0 <= inp.payment_processing_fee_percent <= 0.50):
        errors.append("Payment processing fee percent must be between 0% and 50%. fraction.")

    return len(errors) == 0, errors
