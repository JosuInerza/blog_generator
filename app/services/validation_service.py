from typing import List, Tuple


def validate_title_and_description(title: str, description: str | None = None) -> Tuple[List[dict], List[str]]:
    """Validate title and optional description.

    Returns a tuple: (errors, warnings)
    - errors: list of dicts with keys `field` and `message` (validation failures)
    - warnings: list of warning messages (non-fatal recommendations)
    """
    errors: List[dict] = []
    warnings: List[str] = []

    if title is None:
        errors.append({"field": "title", "message": "Title is required."})
        return errors, warnings

    title_trimmed = title.strip()
    if len(title_trimmed) < 3 or len(title_trimmed) > 200:
        errors.append({"field": "title", "message": "Title must be between 3 and 200 characters after trimming."})

    import re
    if not re.search(r"[A-Za-z0-9]", title_trimmed):
        errors.append({"field": "title", "message": "Title must contain at least one alphanumeric character."})

    if description:
        desc_trimmed = description.strip()
        if len(desc_trimmed) < 50:
            warnings.append("Description is shorter than the recommended 50 characters.")
        if len(desc_trimmed) > 320:
            warnings.append("Description is longer than the recommended 320 characters.")

    return errors, warnings
