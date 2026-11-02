import time
from typing import Dict
from urllib.parse import urlparse

# Track per-domain request timestamps to enforce gentle rate limits
_DOMAIN_LAST_REQUEST: Dict[str, float] = {}
MIN_DOMAIN_INTERVAL = 0.5  # seconds between requests to same domain


def check_crawl_permitted(url: str) -> tuple[bool, str]:
    """
    Check if URL access is permitted under MarketPulse research policy.
    Never bypass authentication, login pages, or obvious admin/paywall routes.
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.lower()
        blocked_keywords = [
            "/login", "/signin", "/auth/", "/admin/", "/checkout",
            "/cart", "/wp-login.php", "/user/login", "/session/"
        ]
        for keyword in blocked_keywords:
            if keyword in path:
                return False, f"Blocked by policy: path contains restricted keyword '{keyword}'"
        return True, "permitted"
    except Exception as exc:
        return True, f"Policy check default permitted: {exc}"


def rate_limit_domain(url: str):
    """Enforce non-intrusive rate limiting per domain."""
    try:
        domain = urlparse(url).netloc.lower()
        now = time.time()
        last_req = _DOMAIN_LAST_REQUEST.get(domain, 0.0)
        elapsed = now - last_req
        if elapsed < MIN_DOMAIN_INTERVAL:
            time.sleep(MIN_DOMAIN_INTERVAL - elapsed)
        _DOMAIN_LAST_REQUEST[domain] = time.time()
    except Exception:
        pass
