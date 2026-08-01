"""Tests for the storage and database layer."""

import pytest

from src.database.models import Base
from src.database.session import create_engine, create_session
from src.models.job import Job
from src.storage.repository import JobRepository


@pytest.fixture()
def session():
    """Create an in-memory SQLite session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = create_session(engine)
    test_session = session_factory()
    yield test_session
    test_session.close()


def make_job(**overrides) -> Job:
    """Create a valid Job with test defaults."""
    defaults = {
        "title": "Software Engineer",
        "company": "Acme Corp",
        "description": "Build cool stuff.",
        "url": "https://example.com/jobs/123",
        "salary_min": 50000.0,
        "salary_max": 80000.0,
        "salary_currency": "USD",
        "location": "Ho Chi Minh City",
        "employment_type": "full_time",
        "experience_level": "senior",
        "source": "example_site",
        "source_id": "https://example.com/jobs/123",
    }
    defaults.update(overrides)
    return Job(**defaults)


def test_save_job(session) -> None:
    """A job is saved and retrievable."""
    repo = JobRepository(session)
    job = make_job()

    record = repo.save(job)

    assert record.id is not None
    assert record.title == "Software Engineer"
    assert record.company == "Acme Corp"
    assert record.source == "example_site"


def test_upsert_updates_existing(session) -> None:
    """Upsert updates an existing record by (source, source_id)."""
    repo = JobRepository(session)
    job = make_job(title="Original Title")

    repo.save(job)

    updated_job = make_job(title="Updated Title")
    record = repo.upsert(updated_job)

    assert record.title == "Updated Title"
    assert repo.find_all().__len__() == 1


def test_upsert_inserts_new(session) -> None:
    """Upsert inserts a new record when none exists."""
    repo = JobRepository(session)
    job = make_job()

    record = repo.upsert(job)

    assert record.id is not None
    assert repo.find_all().__len__() == 1


def test_find_by_source_id(session) -> None:
    """A record is found by source and source_id."""
    repo = JobRepository(session)
    job = make_job()
    repo.save(job)

    found = repo.find_by_source_id("example_site", "https://example.com/jobs/123")

    assert found is not None
    assert found.title == "Software Engineer"


def test_find_by_source_id_not_found(session) -> None:
    """None is returned when no record matches."""
    repo = JobRepository(session)

    found = repo.find_by_source_id("example_site", "nonexistent")

    assert found is None


def test_find_all(session) -> None:
    """All records are returned."""
    repo = JobRepository(session)
    repo.save(make_job(source_id="https://example.com/jobs/1"))
    repo.save(make_job(source_id="https://example.com/jobs/2"))

    records = repo.find_all()

    assert len(records) == 2