# Task 011 — QueryMapper

## Status

done

## Description

Implement a QueryMapper module to support keyword-based job searching.

The purpose is to map a logical job category into one or more search keywords before scraping.

## Requirements

- Create `src/core/query_mapper.py` with:
  - A `QueryMapper` class:
    - `map(category: str) -> list[str]` — maps a logical job category to search keywords.
  - Built-in category mappings (extensible):
    - `"it"` → `["backend", "frontend", "fullstack", "software engineer", "devops"]`
    - `"marketing"` → `["marketing", "digital marketing", "content marketing"]`
    - `"sales"` → `["sales", "kinh doanh", "business development"]`
  - Unknown categories return `[category]` (the category itself as a keyword).
- Integrate QueryMapper into the existing scraping flow:
  - The pipeline should accept a category and use QueryMapper to get keywords.
  - Each keyword should be used to build a search URL for scraping.
- Add documentation for QueryMapper in `docs/features/query_mapper.md` (update the existing doc).
- Create unit tests in `tests/test_query_mapper.py`:
  - Known category maps to multiple keywords.
  - Unknown category returns itself.
  - QueryMapper is extensible (can add new mappings).

## Definition of Done

- `src/core/query_mapper.py` exists with `QueryMapper`.
- QueryMapper is integrated into the pipeline.
- Tests cover known, unknown, and extensible cases.
- All tests pass with pytest.
- Documentation is updated.
- Committed to Git with message: `feat: add query mapper`