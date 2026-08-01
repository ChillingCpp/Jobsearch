# Task 010 — TopCV Configuration

## Status

done

## Description

Add the first real website configuration for TopCV (https://www.topcv.vn).

This validates the configuration-driven architecture end-to-end with a real recruitment website.

## Requirements

- Create `configs/topcv.yaml` with:
  - `name: topcv`
  - `start_url: https://www.topcv.vn/viec-lam`
  - Selectors for job listings on TopCV:
    - `job_listing`
    - `title`
    - `company`
    - `description`
    - `url`
    - `salary`
    - `location`
    - `posted_date`
  - Pagination rules if applicable.
  - Request headers with a reasonable User-Agent.
- Verify the config loads correctly with `load_config`.
- Run the pipeline against the config (may fail due to network/anti-bot — this is acceptable; the config should be structurally valid).

## Notes

- TopCV selectors may change over time. If the selectors are wrong, the parser will return empty strings (not errors), which is the designed behavior.
- This task validates that adding a new website requires only a config file — no code changes.

## Definition of Done

- `configs/topcv.yaml` exists.
- The config loads successfully with `load_config`.
- No core engine code was modified.
- Committed to Git with message: `feat: support TopCV configuration`