# Task 006 — Normalizer

## Status

done

## Description

Implement the normalizer module.

The normalizer is responsible for transforming raw values into standardized values.

Examples:

- Salary
- Location
- Employment type
- Experience level
- Dates

Normalization should be independent from website implementations.

## Requirements

- Create `src/normalizer/normalizer.py` with:
  - A `Normalizer` class:
    - `normalize(raw: RawJob, source: str) -> Job` — converts a `RawJob` into a validated `Job`.
  - Normalization rules:
    - **Salary**: parse strings like `"$50,000 - $80,000"`, `"50-80 triệu"`, `"Thỏa thuận"` (negotiable → None), `"1000 USD"` into `salary_min`, `salary_max`, `salary_currency`.
    - **Location**: trim whitespace; empty string stays empty.
    - **Employment type**: map common Vietnamese/English terms to a standard set (`full_time`, `part_time`, `contract`, `internship`, `remote`).
    - **Experience level**: map common terms to a standard set (`entry`, `junior`, `mid`, `senior`, `lead`, `manager`).
    - **Posted date**: parse common date formats into a `datetime`; if unparseable, leave as `None`.
  - The `source` and `source_id` fields on the Job come from the config name and the raw URL.
- Create unit tests in `tests/test_normalizer.py`:
  - Salary parsing (ranges, single values, negotiable, currency).
  - Employment type mapping.
  - Experience level mapping.
  - Date parsing.
  - Full normalization produces a valid Job.

## Definition of Done

- `src/normalizer/normalizer.py` exists with `Normalizer`.
- Tests cover salary, employment type, experience, dates, and full normalization.
- All tests pass with pytest.
- Normalizer is independent of website implementations.
- Committed to Git with message: `feat: add normalizer`