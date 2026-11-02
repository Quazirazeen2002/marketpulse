from datetime import datetime, timezone
from typing import Optional, Tuple
from dateutil import parser


def evaluate_freshness(
    date_str: Optional[str],
    time_horizon: str = "Current",
    is_pricing_or_campaign: bool = False,
) -> Tuple[float, str]:
    """
    Evaluate source freshness on a 0-100 scale.
    Domain-sensitive: fast-moving topics (pricing, promotional campaigns) decay quickly,
    whereas structural market data or macroeconomic research decay more slowly.
    """
    if not date_str:
        return 50.0, "Publication date is unknown; evaluated with neutral freshness baseline."

    try:
        parsed_dt = parser.parse(str(date_str))
        if not parsed_dt.tzinfo:
            parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)
        now_dt = datetime.now(timezone.utc)
        days_old = max(0, (now_dt - parsed_dt).days)
    except Exception:
        return 50.0, f"Unable to parse publication date '{date_str}'; neutral freshness assigned."

    # Pricing & promotions: high volatility
    if is_pricing_or_campaign or "current" in time_horizon.lower():
        if days_old <= 90:
            return 98.0, f"Very fresh: published within last 3 months ({days_old} days ago)."
        elif days_old <= 365:
            return 82.0, f"Recent: published within last year ({days_old} days ago)."
        elif days_old <= 730:
            return 65.0, f"Moderately recent: published within 2 years ({days_old} days ago)."
        elif days_old <= 1460:
            return 45.0, f"Aging source: published {days_old // 365} years ago; verify current status."
        else:
            return 25.0, f"Historical source: published {days_old // 365} years ago; may not reflect current market conditions."

    # Macro & market structure: lower volatility
    if days_old <= 365:
        return 95.0, f"High freshness: published within last 12 months ({days_old} days ago)."
    elif days_old <= 1095:  # 3 years
        return 80.0, f"Adequate freshness: published within last 3 years ({days_old} days ago)."
    else:
        return 55.0, f"Historical baseline: published {days_old // 365} years ago; relevant for structural context."
