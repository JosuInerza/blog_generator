import re
import time
import unicodedata
from typing import Set

_used_slugs: Set[str] = set()

def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii")

def generate_slug(title: str) -> str:
    if title is None:
        return ""
    text = _strip_accents(title)
    text = text.lower().strip()
    # replace separators and whitespace with hyphen
    text = re.sub(r"[\s_–—]+", "-", text)
    # remove invalid characters (keep a-z, 0-9 and hyphen)
    text = re.sub(r"[^a-z0-9-]", "", text)
    # collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text

def ensure_unique(slug: str) -> str:
    if not slug:
        slug = f"post-{int(time.time())}"

    base = slug
    candidate = base
    counter = 1
    while candidate in _used_slugs:
        counter += 1
        candidate = f"{base}-{counter}"
    _used_slugs.add(candidate)
    return candidate

def clear_store() -> None:
    """Clear the in-memory slug store (useful for tests)."""
    _used_slugs.clear()
