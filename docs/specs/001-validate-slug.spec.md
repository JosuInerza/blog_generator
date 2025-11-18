---
specId: 001-validate-slug
title: Validate Title & Generate Unique Slug
relatedPRD: /docs/PRD.md
---

# 001-validate-slug.spec.md

## 1. Problem Specification

### Summary

Content editors and automation tools need a simple, deterministic API to validate blog post titles and optional descriptions for SEO best-practices and receive a canonical URL slug. The service must return clear validation errors and produce unique, URL-safe slugs.

### User Stories

- User Story 1 — Validate Title
  - As a Content Editor
  - I want to submit a title and get back validation results
  - So that I know whether the title meets SEO and application constraints before publishing

- User Story 2 — Generate Slug
  - As a Content Editor or Integrator
  - I want the system to return a deterministic, URL-safe slug for a given title
  - So that I can use that slug for URLs and routing

- User Story 3 — Uniqueness Guarantee
  - As a Backend Integrator
  - I want slugs to be unique in the storage context, with numeric suffixing on collisions
  - So that URLs do not conflict and older content remains reachable

### Scope and Constraints

- Minimal initial scope: implement `POST /validate` endpoint that validates `title` and optional `description` and returns `{ valid, slug, warnings? }`.
- Persistence is optional for the minimal feature; uniqueness can be demonstrated using an in-memory store for tests. Persistence can be added later.
- Implement using Python 3.10+, FastAPI and Pydantic.

## 2. Solution Design

### Overview

Implement a small FastAPI service component that exposes `POST /validate`. The route validates incoming payloads using Pydantic schemas and produces a slug using a deterministic algorithm. A service layer handles slug generation and uniqueness checks; tests cover edge cases.

### Data Models

- Request: `ValidateRequest`
  - `title`: string (required)
  - `description`: string (optional)

- Response: `ValidateResponse`
  - `valid`: boolean
  - `slug`: string (generated, present when `valid` is true)
  - `warnings`: list[string] (optional)
  - `errors`: list[{ field, message }] (present on validation failure)

### Slug Generation Algorithm (detailed)

1. Normalize to Unicode NFC and convert to lowercase.
2. Trim leading/trailing whitespace.
3. Replace any run of whitespace or separator characters (spaces, underscores, em-dash, en-dash, punctuation commonly used as separators) with a single hyphen (`-`).
4. Remove all characters except ASCII a-z, 0-9 and hyphen. (Optionally use transliteration for accented characters — simplest approach: strip accents using Unicode normalization + ASCII transliteration.)
5. Collapse multiple hyphens to one.
6. Remove leading/trailing hyphens.
7. If the resulting slug is empty, fall back to `post` + timestamp or a configurable placeholder.
8. Uniqueness: check existing slugs in the chosen store; if collision, append `-2`, `-3`, ... incrementing until unique.

### Software Components

- API Layer: FastAPI route `POST /validate`.
- Schemas: Pydantic models `ValidateRequest`, `ValidateResponse`, and `ErrorDetail`.
- Service layer: `slug_service` with functions `generate_slug(title)` and `ensure_unique(slug, store)`.
- Store (for uniqueness): simple in-memory set for initial implementation; abstract interface to swap in persistent store later.
- Tests: pytest test suite to validate title rules, slug output, and collision handling.

### API Design

- Endpoint: `POST /validate`
  - Request body: `ValidateRequest` (JSON)
  - Responses:
    - 200 OK: `{ valid: true, slug: "...", warnings?: [] }` when input is valid
    - 422 Unprocessable Entity: `{ detail: "Validation failed", errors: [{ field, message }] }` when Pydantic or business validation fails

### Validation Rules (implementation notes)

- Title:
  - Required, type `str`.
  - After trimming, length must be >= 3 and <= 200.
  - Must contain at least one alphanumeric character (regex check: `[A-Za-z0-9]`).
  - Must not be only control characters or whitespace.

- Description (optional):
  - If provided, trimmed. Recommended length 50–320 characters — return `warnings` if outside recommended range but still accept the request unless configured to enforce.

### Monitoring, Security, and Error Handling

- Monitoring: basic request logging; expose `/metrics` later if needed.
- Security: sanitize inputs; limit request body size; CORS configuration left permissive for localhost and adjustable via settings.
- Error handling: return structured error responses. Catch unexpected exceptions and return 500 with a generic message while logging the stacktrace.

### Test Plan

- Unit tests for title validation (lengths, whitespace, special characters, non-alphanumeric failures).
- Unit tests for slug generation (diacritics, punctuation, spaces -> hyphens, repeated separators, empty title fallback).
- Tests for uniqueness behaviour using an in-memory store.

## 3. Acceptance Criteria

All acceptance criteria use the EARS-style phrasing (SHALL / WHEN / THEN / IF).

- AC1 (Title validation):
  - SHALL validate title on `POST /validate`; WHEN the title is missing or trimmed length < 3 or > 200 or contains no alphanumeric characters, THEN the API SHALL return HTTP 422 with `errors` describing the failing field and reason.

- AC2 (Description warnings):
  - SHALL accept an optional description; WHEN the description length is outside 50–320 characters, THEN the API SHALL return 200 with `warnings` describing the recommendation (not an error).

- AC3 (Slug deterministic generation):
  - SHALL generate a slug deterministically from title using the algorithm above; WHEN a title with equivalent semantics is supplied, THEN the slug SHALL be identical (modulo uniqueness suffix).

- AC4 (Uniqueness handling):
  - SHALL ensure slugs are unique within the configured store; WHEN a generated slug collides with an existing slug, THEN the API SHALL append a numeric suffix (`-2`, `-3`, ...) to produce a unique slug and return it.

- AC5 (Empty or invalid resulting slug):
  - SHALL fallback to a safe placeholder slug when the cleaned title produces an empty slug; WHEN this occurs, THEN the API SHALL return a slug in the format `post-<timestamp>` or configured placeholder.

- AC6 (Tests):
  - SHALL include unit tests for validation, slug generation and uniqueness; WHEN running `pytest`, THEN all tests shall pass.

---

### Implementation Notes & Next Steps

1. Implement `POST /validate` and supporting service and schema files under `app/`.
2. Add unit tests in `tests/` for validation and slug behaviour.
3. Optionally, implement persistence and `/posts` CRUD endpoints later.

---

End of specification `001-validate-slug`
