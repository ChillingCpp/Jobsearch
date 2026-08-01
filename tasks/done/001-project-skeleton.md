# Task 001 — Project Skeleton

## Status

done

## Description

Set up the initial project skeleton for the job aggregation system.

This includes the folder structure defined in the project plan, the dependency file, a README, and empty module stubs so the architecture is visible and pytest is ready.

## Requirements

- Create the folder structure per `docs/project_plan.md`:
  - `src/core/`
  - `src/crawler/`
  - `src/parser/`
  - `src/normalizer/`
  - `src/storage/`
  - `src/database/`
  - `src/scheduler/`
  - `src/models/`
  - `src/utils/`
  - `src/main.py`
  - `tests/`
  - `configs/`
- Create `requirements.txt` with the technology stack dependencies.
- Create `README.md` describing the project briefly.
- Create empty `__init__.py` files for each package so imports work.
- Create a minimal `main.py` entry point stub.
- Set up pytest with a placeholder test.

## Definition of Done

- Folder structure exists.
- `requirements.txt` exists.
- `README.md` exists.
- Module stubs exist.
- `main.py` stub exists.
- A placeholder test passes with pytest.
- Committed to Git with message: `feat: set up project skeleton`