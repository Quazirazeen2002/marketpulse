"""
Business Scenario Simulator Package for MARKETPULSE Stage 2.
"""

from app.services.business_simulation.calculator import calculate_scenario
from app.services.business_simulation.break_even import calculate_break_even_metrics
from app.services.business_simulation.sensitivity import run_sensitivity_analysis
from app.services.business_simulation.scenarios import build_scenario_suite, generate_scenario_suite
from app.services.business_simulation.validation import validate_scenario_input
from app.services.business_simulation.models import (
    ScenarioInput,
    ScenarioResult,
    SensitivityAnalysis,
    BusinessScenario,
)

__all__ = [
    "calculate_scenario",
    "calculate_break_even_metrics",
    "run_sensitivity_analysis",
    "build_scenario_suite",
    "generate_scenario_suite",
    "validate_scenario_input",
    "ScenarioInput",
    "ScenarioResult",
    "SensitivityAnalysis",
    "BusinessScenario",
]
