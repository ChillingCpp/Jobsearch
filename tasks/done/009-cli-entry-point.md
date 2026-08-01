# Task 009 — CLI / Entry Point

## Status

done

## Description

Implement the CLI entry point that runs the full pipeline.

The pipeline flow:

```
Load configs
   ↓
For each config:
   Crawl HTML
   ↓
   Parse raw jobs
   ↓
   Normalize to Job
   ↓
   Store in database
```

## Requirements

- Update `src/main.py` to:
  - Accept command-line arguments:
    - `--configs` (path to configs directory, default `configs/`)
    - `--database` (database URL, default `sqlite:///jobs.db`)
    - `--once` (run the pipeline once)
    - `--interval` (run the pipeline repeatedly at the given interval in seconds)
  - Load all website configs.
  - For each config:
    - Fetch HTML using `Fetcher`.
    - Parse raw jobs using `Parser`.
    - Normalize each raw job using `Normalizer`.
    - Store each job using `JobRepository`.
  - Use the `Scheduler` to run once or at intervals.
- Create `src/core/pipeline.py` with:
  - A `run_pipeline(configs, fetcher, parser, normalizer, repository)` function that processes all configs through the pipeline.
- Create unit tests in `tests/test_pipeline.py`:
  - The pipeline processes a config end-to-end with mocked fetcher.
  - The pipeline stores normalized jobs in the repository.

## Notes

- Use `argparse` for CLI parsing (no external dependencies).
- Keep the pipeline function simple and focused.
- The pipeline should handle a config with no jobs gracefully.

## Definition of Done

- `src/core/pipeline.py` exists with `run_pipeline`.
- `src/main.py` uses argparse and runs the pipeline.
- Tests cover end-to-end pipeline with mocked fetcher.
- All tests pass with pytest.
- Committed to Git with message: `feat: add cli entry point`