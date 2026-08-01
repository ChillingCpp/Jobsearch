# Task 002 — Data Models

## Status

done

## Description

Define the normalized data models for the job aggregation system using Pydantic.

These models are the unified format that the normalizer produces and the database stores.

They must be independent of any specific website.

## Requirements

- Create `src/models/job.py` with a `Job` model.
- Fields to include (normalized):
  - `title`
  - `company`
  - `description`
  - `url`
  - `salary_min` / `salary_max` / `salary_currency`
  - `location`
  - `employment_type`
  - `experience_level`
  - `posted_date`
  - `source` (website name)
  - `source_id` (unique ID on the source website)
  - `created_at`
  - `updated_at`
- Use Pydantic for validation.
- Use sensible defaults and optional fields where appropriate.
- Add unit tests for the model in `tests/test_models.py`.

## Definition of Done

- `src/models/job.py` exists with a validated `Job` model.
- Tests cover creation, validation, and defaults.
- All tests pass with pytest.
- Follows project architecture (models are website-independent).
- Committed to Git with message: `feat: add job data model`