"""
Break-Even Analysis & Unit Economics Module for Business Simulation.
"""

import math
from typing import Dict, Any


def calculate_break_even_metrics(
    selling_price: float,
    unit_cost: float,
    variable_cost_per_order: float,
    fixed_costs: float,
) -> Dict[str, Any]:
    """Calculate explicit unit contribution and break-even point."""
    unit_contribution = selling_price - unit_cost - variable_cost_per_order
    if unit_contribution <= 0:
        return {
            "unit_contribution": round(unit_contribution, 2),
            "break_even_units": -1,
            "break_even_revenue": -1.0,
            "status": "unviable_unit_economics",
        }

    be_units = int(math.ceil(fixed_costs / unit_contribution))
    be_revenue = round(be_units * selling_price, 2)
    return {
        "unit_contribution": round(unit_contribution, 2),
        "break_even_units": be_units,
        "break_even_revenue": be_revenue,
        "status": "achievable",
    }
