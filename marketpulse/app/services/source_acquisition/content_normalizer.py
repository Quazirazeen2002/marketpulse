import hashlib
import re
import unicodedata
from typing import Tuple


def normalize_content_text(text: str) -> str:
    """Normalize extracted text, strip excessive whitespace, and remove noise."""
    if not text:
        return ""

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Normalize carriage returns and tabs
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse horizontal spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive repeated blank lines (keep at most 2 newlines)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # Strip leading/trailing whitespace
    return text.strip()


def compute_content_hash(text: str) -> str:
    """Compute sha256 content hash of normalized text for deduplication."""
    clean = normalize_content_text(text).lower()
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def truncate_text(text: str, max_chars: int = 12000) -> Tuple[str, bool]:
    """Truncate excessively long source documents to preserve memory/tokens."""
    clean = normalize_content_text(text)
    if len(clean) > max_chars:
        return clean[:max_chars] + "\n\n[... content truncated to limit ...]", True
    return clean, False
