from fastapi import APIRouter, HTTPException
from app.schemas import ValidateRequest, ValidateResponse, ErrorDetail
from app.services.slug_service import generate_slug, ensure_unique

router = APIRouter()


@router.post("/validate", response_model=ValidateResponse)
def validate_title(payload: ValidateRequest):
    errors = []
    title = payload.title or ""
    title_trimmed = title.strip()
    if len(title_trimmed) < 3 or len(title_trimmed) > 200:
        errors.append(ErrorDetail(field="title", message="Title must be between 3 and 200 characters after trimming."))
    import re
    if not re.search(r"[A-Za-z0-9]", title_trimmed):
        errors.append(ErrorDetail(field="title", message="Title must contain at least one alphanumeric character."))

    if errors:
        raise HTTPException(status_code=422, detail={"detail": "Validation failed", "errors": [e.dict() for e in errors]})

    warnings = []
    description = (payload.description or "").strip()
    if description:
        if len(description) < 50:
            warnings.append("Description is shorter than the recommended 50 characters.")
        if len(description) > 320:
            warnings.append("Description is longer than the recommended 320 characters.")

    raw_slug = generate_slug(title_trimmed)
    unique_slug = ensure_unique(raw_slug)

    return ValidateResponse(valid=True, slug=unique_slug, warnings=warnings or None)
