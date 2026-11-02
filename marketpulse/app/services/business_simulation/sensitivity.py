"""
Sensitivity Analysis Module for Business Simulation.
Tests elasticity across Price, Order Volume, Marketing, Delivery Cost, and Return Rate.
"""

from typing import List, Dict, Any
from app.schemas.strategic import ScenarioInput, SensitivityAnalysis
from app.services.business_simulation.calculator import calculate_scenario


def run_sensitivity_analysis(base_input: ScenarioInput) -> List[SensitivityAnalysis]:
    """
    Run 5-dimensional sensitivity variations (-20%, -10%, baseline, +10%, +20%)
    across key business levers.
    """
    results: List[SensitivityAnalysis] = []
    delta_multipliers = [0.80, 0.90, 1.0, 1.10, 1.20]

    # 1. Price Sensitivity
    price_variations = []
    for m in delta_multipliers:
        adj_price = round(base_input.product_selling_price * m, 2)
        # Avoid cost exceeding price in test
        if adj_price <= base_input.product_cost:
            continue
        test_inp = base_input.model_copy(update={"product_selling_price": adj_price})
        res = calculate_scenario(test_inp)
        price_variations.append({
            "percentage_change": f"{(m - 1.0) * 100:+.0f}%",
            "tested_value": adj_price,
            "monthly_operating_profit": res.monthly_operating_profit,
            "break_even_orders": res.break_even_orders,
        })
    results.append(SensitivityAnalysis(
        variable_tested="Product Selling Price",
        baseline_value=base_input.product_selling_price,
        variations=price_variations,
    ))

    # 2. Volume Sensitivity
    vol_variations = []
    for m in delta_multipliers:
        adj_vol = int(round(base_input.expected_monthly_orders * m))
        test_inp = base_input.model_copy(update={"expected_monthly_orders": adj_vol})
        res = calculate_scenario(test_inp)
        vol_variations.append({
            "percentage_change": f"{(m - 1.0) * 100:+.0f}%",
            "tested_value": float(adj_vol),
            "monthly_operating_profit": res.monthly_operating_profit,
            "break_even_orders": res.break_even_orders,
        })
    results.append(SensitivityAnalysis(
        variable_tested="Monthly Order Volume",
        baseline_value=float(base_input.expected_monthly_orders),
        variations=vol_variations,
    ))

    # 3. Return / Refund Rate Sensitivity
    ret_variations = []
    for delta in [-0.04, -0.02, 0.0, +0.02, +0.05]:
        adj_ret = max(0.01, min(0.40, round(base_input.return_refund_rate + delta, 3)))
        test_inp = base_input.model_copy(update={"return_refund_rate": adj_ret})
        res = calculate_scenario(test_inp)
        ret_variations.append({
            "percentage_change": f"{delta * 100:+.0f}% pts",
            "tested_value": adj_ret,
            "monthly_operating_profit": res.monthly_operating_profit,
            "break_even_orders": res.break_even_orders,
        })
    results.append(SensitivityAnalysis(
        variable_tested="Return/Refund Rate",
        baseline_value=base_input.return_refund_rate,
        variations=ret_variations,
    ))

    # 4. Marketing Expenditure Sensitivity
    mkt_variations = []
    for m in delta_multipliers:
        adj_mkt = round(base_input.monthly_marketing_expenditure * m, 2)
        test_inp = base_input.model_copy(update={"monthly_marketing_expenditure": adj_mkt})
        res = calculate_scenario(test_inp)
        mkt_variations.append({
            "percentage_change": f"{(m - 1.0) * 100:+.0f}%",
            "tested_value": adj_mkt,
            "monthly_operating_profit": res.monthly_operating_profit,
            "break_even_orders": res.break_even_orders,
        })
    results.append(SensitivityAnalysis(
        variable_tested="Monthly Marketing Expenditure",
        baseline_value=base_input.monthly_marketing_expenditure,
        variations=mkt_variations,
    ))

    # 5. Delivery Cost Sensitivity
    deliv_variations = []
    for m in delta_multipliers:
        adj_deliv = max(0.5, round(base_input.delivery_cost_per_order * m, 2))
        test_inp = base_input.model_copy(update={"delivery_cost_per_order": adj_deliv})
        res = calculate_scenario(test_inp)
        deliv_variations.append({
            "percentage_change": f"{(m - 1.0) * 100:+.0f}%",
            "tested_value": adj_deliv,
            "monthly_operating_profit": res.monthly_operating_profit,
            "break_even_orders": res.break_even_orders,
        })
    results.append(SensitivityAnalysis(
        variable_tested="Delivery Cost per Order",
        baseline_value=base_input.delivery_cost_per_order,
        variations=deliv_variations,
    ))

    return results
