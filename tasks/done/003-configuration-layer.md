# Task 003 — Configuration Layer

## Status

done

## Description

Build the configuration loading system.

This layer is responsible for loading YAML website configurations.

Each website configuration defines:

- Selectors (CSS / XPath)
- Pagination rules
- Browser actions
- Extraction rules

The configuration layer must NOT contain business logic.

## Requirements

- Create `src/core/config.py` with:
  - A `WebsiteConfig` model (Pydantic) describing a website configuration:
    - `name`
    - `start_url`
    - `selectors` (CSS selectors for job fields)
    - `pagination` (optional rules)
    - `browser_actions` (optional list of actions)
    - `request_headers` (optional)
  - A `load_config(path)` function that reads a YAML file and returns a validated `WebsiteConfig`.
  - A `load_all_configs(config_dir)` function that loads every YAML file in a directory.
- Create an example config `configs/example.yaml`.
- Create unit tests in `tests/test_config.py`:
  - Loading a valid YAML config.
  - Loading a missing file raises an error.
  - Loading an invalid config raises a validation error.

## Definition of Done

- `src/core/config.py` exists.
- `configs/example.yaml` exists.
- Tests cover loading, missing file, and invalid config.
- All tests pass with pytest.
- Follows project architecture (configuration layer has no business logic).
- Committed to Git with message: `feat: add configuration layer`