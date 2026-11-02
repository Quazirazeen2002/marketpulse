from urllib.parse import urlparse
from typing import Tuple

# Curated reputable domain authority lists
GOV_AND_ACADEMIC_TLDS = (".gov", ".edu", ".ac.bd", ".gov.bd", ".org", ".int")

HIGH_AUTHORITY_DOMAINS = {
    # International & Industry Data
    "worldbank.org", "imf.org", "reuters.com", "bloomberg.com", "statista.com",
    "ft.com", "forbes.com", "mckinsey.com", "bain.com", "gartner.com",
    "globenewswire.com", "prnewswire.com", "businesswire.com", "wikipedia.org",
    # Bangladesh Reputable Media & Commercial Sources
    "tbsnews.net", "thedailystar.net", "thefinancialexpress.com.bd",
    "dhakatribune.com", "prothomalo.com", "bb.org.bd", "epb.gov.bd",
    "nbr.gov.bd", "bida.gov.bd", "lightcastlebd.com", "futurestartup.com",
    "dailycapitalviews.com",
}

MEDIUM_AUTHORITY_DOMAINS = {
    "6wresearch.com", "accio.com", "bipony.com", "theincap.com", "case48.com",
    "linkedin.com", "medium.com", "substack.com", "businessinspection.com.bd",
}


def evaluate_publisher_credibility(url: str, publisher: str = "") -> Tuple[float, str]:
    """
    Evaluate publisher credibility on a 0-100 scale based on domain provenance,
    institutional authority, and publication standards.
    """
    if not url:
        return 20.0, "No URL provided; unverified source."

    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
    except Exception:
        domain = "unknown"

    # 1. Government, Academic, or International Institutional sources
    for tld in GOV_AND_ACADEMIC_TLDS:
        if domain.endswith(tld):
            return 95.0, f"High institutional credibility: official institutional/governmental domain ({tld})."

    # 2. Known High Authority Business & News Portals
    if domain in HIGH_AUTHORITY_DOMAINS:
        return 88.0, f"High editorial credibility: reputable news or institutional research publisher ({domain})."

    # 3. Known Industry Research & Business Intelligence Sites
    if domain in MEDIUM_AUTHORITY_DOMAINS:
        return 72.0, f"Moderate credibility: industry trade portal or market intelligence site ({domain})."

    # 4. Standard Commercial / Company Websites
    if domain.endswith(".com") or domain.endswith(".net") or domain.endswith(".org"):
        return 58.0, f"Standard commercial web source ({domain}); secondary verification advised."

    return 45.0, f"Unverified web domain ({domain}); evaluate evidence conservatively."
