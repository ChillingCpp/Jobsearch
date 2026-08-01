# Task 007 — Storage / Database

## Status

done

## Description

Implement the storage and database layer.

The storage layer is responsible for saving and loading job data.

Responsibilities:

- Store jobs
- Update existing records
- Query data

The storage layer should hide database implementation details.

## Requirements

- Create `src/database/models.py` with:
  - A SQLAlchemy `JobRecord` model matching the `Job` Pydantic model fields.
- Create `src/storage/repository.py` with:
  - A `JobRepository` class:
    - `__init__(session)` — accepts a SQLAlchemy session.
    - `save(job: Job) -> JobRecord` — inserts a new job record.
    - `upsert(job: Job) -> JobRecord` — updates an existing record by `(source, source_id)` or inserts a new one.
    - `find_by_source_id(source: str, source_id: str) -> JobRecord | None` — finds a record.
    - `find_all() -> list[JobRecord]` — returns all records.
- Create `src/database/session.py` with:
  - `create_engine(database_url: str)` — creates a SQLAlchemy engine.
  - `create_session(engine)` — creates a session factory.
- Create unit tests in `tests/test_storage.py`:
  - Save a job and verify it's stored.
  - Upsert updates an existing record.
  - Find by source and source_id.
  - Find all returns all records.

## Notes

- Use SQLite in-memory for tests (no PostgreSQL required for unit tests).
- Keep the repository simple and focused on CRUD operations.

## Definition of Done

- `src/database/models.py` exists with `JobRecord`.
- `src/database/session.py` exists with engine/session helpers.
- `src/storage/repository.py` exists with `JobRepository`.
- Tests cover save, upsert, find, and find_all.
- All tests pass with pytest.
- Storage hides database implementation details.
- Committed to Git with message: `feat: add storage and database layer`