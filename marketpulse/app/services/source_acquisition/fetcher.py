import logging
from typing import Tuple, Optional
import httpx
from .robots_policy import check_crawl_permitted, rate_limit_domain
from .url_validator import is_valid_http_url

logger = logging.getLogger(__name__)

USER_AGENT = "MARKETPULSE-Research-Engine/1.0 (+https://marketpulse.ai/bot; enterprise-business-intelligence)"
DEFAULT_TIMEOUT = httpx.Timeout(connect=10.0, read=15.0, write=10.0, pool=10.0)
MAX_RESPONSE_BYTES = 10 * 1024 * 1024  # 10 MB limit


def fetch_url(url: str) -> Tuple[Optional[bytes], str, Optional[int], Optional[str]]:
    """
    Fetch remote web content with bounded timeouts, redirect tracking, and safety limits.
    Returns: (content_bytes, content_type, http_status, error_message)
    """
    if not is_valid_http_url(url):
        return None, "", None, f"Invalid URL format: '{url}'"

    permitted, reason = check_crawl_permitted(url)
    if not permitted:
        return None, "", None, reason

    rate_limit_domain(url)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/pdf,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    try:
        with httpx.Client(
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
            max_redirects=5,
            verify=True,
        ) as client:
            response = client.get(url, headers=headers)
            http_status = response.status_code

            if response.status_code >= 400:
                return None, "", http_status, f"HTTP Error {response.status_code}: {response.reason_phrase}"

            content_type = response.headers.get("content-type", "").lower()
            content_bytes = response.content

            if len(content_bytes) > MAX_RESPONSE_BYTES:
                content_bytes = content_bytes[:MAX_RESPONSE_BYTES]

            return content_bytes, content_type, http_status, None

    except httpx.TimeoutException:
        return None, "", None, "Connection or read timed out"
    except httpx.ConnectError as exc:
        return None, "", None, f"Connection failed: {exc}"
    except httpx.HTTPStatusError as exc:
        return None, "", exc.response.status_code, str(exc)
    except Exception as exc:
        return None, "", None, f"Fetch error: {exc}"
