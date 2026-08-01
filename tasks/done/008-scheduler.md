# Task 008 — Scheduler

## Status

done

## Description

Implement the scheduler module.

The scheduler is responsible for deciding when crawling should happen.

Examples:

- Manual crawl
- Daily crawl
- Hourly crawl

The scheduler should not crawl or parse itself — it only triggers the pipeline.

## Requirements

- Create `src/scheduler/scheduler.py` with:
  - A `Scheduler` class:
    - `__init__(job_function: Callable[[], None])` — accepts a callable that runs the crawl pipeline.
    - `run_once()` — runs the job function once (manual crawl).
    - `run_every(interval_seconds: int)` — runs the job function repeatedly at the given interval.
    - `stop()` — stops the scheduled execution.
  - The scheduler should be simple and not depend on external scheduling libraries.
- Create unit tests in `tests/test_scheduler.py`:
  - `run_once` calls the job function exactly once.
  - `run_every` calls the job function multiple times at the interval.
  - `stop` halts the scheduled execution.

## Notes

- Use `threading.Timer` or a simple loop with `time.sleep` for the interval.
- Keep the scheduler minimal — no cron expressions or complex scheduling.

## Definition of Done

- `src/scheduler/scheduler.py` exists with `Scheduler`.
- Tests cover run_once, run_every, and stop.
- All tests pass with pytest.
- Scheduler has no crawling or parsing logic.
- Committed to Git with message: `feat: add scheduler`