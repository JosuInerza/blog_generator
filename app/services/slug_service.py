import re
import time
import unicodedata
from typing import Optional, Set

# Internal default in-memory store for uniqueness checks.
_used_slugs: Set[str] = set()


def _strip_accents(text: str) -> str:
    """Remove diacritics from text using Unicode normalization.

    Keeps ASCII characters; non-ASCII are removed by encoding/decoding.
    """
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("ascii", "ignore").decode("ascii")


def generate_slug(title: Optional[str]) -> str:
    """Generate a URL-friendly slug from a title string.

    Steps:
    - Remove accents
    - Lowercase and trim
    - Replace runs of whitespace/separators with hyphens
    - Remove all characters except a-z, 0-9 and hyphen
    - Collapse multiple hyphens and trim hyphens at ends

    Returns an empty string when title is None or reduces to nothing.
    """
    if not title:
        return ""
    text = _strip_accents(title)
    text = text.lower().strip()
    # replace separators and whitespace with hyphen
    text = re.sub(r"[\s_–—]+", "-", text)
    # remove invalid characters (keep a-z, 0-9 and hyphen)
    text = re.sub(r"[^a-z0-9-]", "", text)
    # collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def ensure_unique(slug: str, store: Optional[Set[str]] = None) -> str:
    """Ensure the provided slug is unique in `store` (defaults to internal memory).

    If `slug` is empty, a fallback of the form `post-<timestamp>` is used.
    If a collision occurs, the function appends `-2`, `-3`, ... until unique.

    Returns the unique slug (and stores it in `store`).
    """
    target_store = store if store is not None else _used_slugs

    if not slug:
        slug = f"post-{int(time.time())}"

    base = slug
    candidate = base
    counter = 1
    while candidate in target_store:
        counter += 1
        candidate = f"{base}-{counter}"
    target_store.add(candidate)
    return candidate


def clear_store(store: Optional[Set[str]] = None) -> None:
    """Clear the given store or the internal in-memory store.

    Useful for tests.
    """
    target_store = store if store is not None else _used_slugs
    target_store.clear()
