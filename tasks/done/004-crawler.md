# Task 004 — Crawler

## Status

done

## Description

Implement the crawler module.

The crawler is responsible for downloading HTML pages.

Responsibilities:

- Download HTML from a URL (using `requests`)
- Handle browser automation when necessary (using Playwright)
- Manage retries and delays
- Return raw HTML

The crawler must NOT parse HTML or write to the database.

## Requirements

- Create `src/crawler/fetcher.py` with:
  - A `Fetcher` class:
    - `fetch(url, headers=None) -> str` — downloads HTML with `requests`, with retry logic and delay between retries.
    - `fetch_with_browser(url, actions=None) -> str` — downloads HTML using Playwright, runs optional browser actions, and returns the page content.
  - Retry behavior:
    - Default: 3 attempts.
    - Delay between attempts: configurable, default 2 seconds.
    - Only retry on failed requests (network errors, timeouts, non-200 status codes).
  - A `__init__` parameter to allow custom retries and delay values.
- All HTTP methods and Playwright usage should be wrapped so the caller only receives HTML text.
- Create unit tests in `tests/test_crawler.py`:
  - Fetch returns HTML from a mock HTTP response.
  - Fetch retries on failure.
  - Fetch raises an exception after exhausting retries.

## Definition of Done

- `src/crawler/fetcher.py` exists with `Fetcher`.
- Tests cover success, retry, and failure cases.
- All tests pass with pytest.
- Crawler has no parsing or database logic.
- Committed to Git with message: `feat: add crawler fetcher`

## Notes

- Use `unittest.mock` to simulate HTTP responses — do not hit real networks in tests.
- Keep the retry logic simple and readable.