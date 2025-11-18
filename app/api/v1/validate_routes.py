from fastapi import APIRouter, HTTPException
from app.schemas import ValidateRequest, ValidateResponse
from app.services.slug_service import generate_slug, ensure_unique
from app.services.validation_service import validate_title_and_description

router = APIRouter()


@router.post("/validate", response_model=ValidateResponse)
def validate_title(payload: ValidateRequest):
    errors, warnings = validate_title_and_description(payload.title, payload.description)

    if errors:
        # Return structured validation payload in the 422 detail
        raise HTTPException(status_code=422, detail={"detail": "Validation failed", "errors": errors})

    raw_slug = generate_slug(payload.title)
    unique_slug = ensure_unique(raw_slug)

    return ValidateResponse(valid=True, slug=unique_slug, warnings=warnings or None)
