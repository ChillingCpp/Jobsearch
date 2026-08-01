# Task 005 — Parser

## Status

done

## Description

Implement the parser module.

The parser is responsible for extracting raw job data from HTML using website configuration.

Responsibilities:

- Read HTML
- Apply website configuration (selectors)
- Produce raw job data

The parser must NOT perform normalization or database operations.

## Requirements

- Create `src/parser/extractor.py` with:
  - A `RawJob` dataclass or Pydantic model with raw fields:
    - `title`
    - `company`
    - `description`
    - `url`
    - `salary`
    - `location`
    - `posted_date`
  - A `Parser` class:
    - `parse(html: str, config: WebsiteConfig) -> list[RawJob]`
  - The parser uses BeautifulSoup with CSS selectors from the config.
  - The `job_listing` selector identifies each job card; the other selectors extract fields from within each card.
  - If a selector is missing or no match is found, the field should be an empty string (not an error).
- Create unit tests in `tests/test_parser.py`:
  - Parsing a simple HTML page with one job listing.
  - Parsing a page with multiple job listings.
  - Parsing a page with missing fields (empty strings).
  - Parsing a page with no job listings (empty list).

## Definition of Done

- `src/parser/extractor.py` exists with `Parser` and `RawJob`.
- Tests cover single, multiple, missing fields, and empty cases.
- All tests pass with pytest.
- Parser has no normalization or database logic.
- Committed to Git with message: `feat: add html parser`