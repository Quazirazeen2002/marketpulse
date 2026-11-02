from urllib.parse import urlparse, urlunparse
from typing import Optional


def normalize_url(url: str) -> str:
    """Normalize URL by stripping fragments, trailing slashes, and lowercasing domain."""
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
        scheme = parsed.scheme.lower()
        if scheme not in ("http", "https"):
            return url.strip()
        netloc = parsed.netloc.lower()
        # Remove standard ports
        if netloc.endswith(":80") and scheme == "http":
            netloc = netloc[:-3]
        elif netloc.endswith(":443") and scheme == "https":
            netloc = netloc[:-4]
        # Clean path: normalize empty to empty, remove trailing slash unless root
        path = parsed.path
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]
        return urlunparse((scheme, netloc, path, parsed.params, parsed.query, ""))
    except Exception:
        return url.strip()


def get_domain(url: str) -> str:
    """Extract clean domain/host from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower() or "unknown_domain"
    except Exception:
        return "unknown_domain"


def is_valid_http_url(url: str) -> bool:
    """Check if URL has valid http/https scheme and domain."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def validate_url(url: str):
    """Validate URL compliance and return (is_valid, reason)."""
    valid = is_valid_http_url(url)
    return valid, ("Compliant" if valid else "Invalid scheme or host")
