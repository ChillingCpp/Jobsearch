"""Tests for the Job data model."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.job import Job


def make_job(**overrides) -> Job:
    """Create a valid Job with test defaults."""
    defaults = {
        "title": "Software Engineer",
        "company": "Acme Corp",
        "description": "Build cool stuff.",
        "url": "https://example.com/jobs/123",
        "salary_min": 50000.0,
        "salary_max": 80000.0,
        "salary_currency": "usd",
        "location": "Ho Chi Minh City",
        "employment_type": "full_time",
        "experience_level": "mid",
        "posted_date": datetime(2026, 1, 1),
        "source": "example_site",
        "source_id": "123",
    }
    defaults.update(overrides)
    return Job(**defaults)


def test_job_creation() -> None:
    """A valid job is created with all fields."""
    job = make_job()

    assert job.title == "Software Engineer"
    assert job.company == "Acme Corp"
    assert str(job.url) == "https://example.com/jobs/123"
    assert job.source == "example_site"
    assert job.source_id == "123"


def test_job_defaults() -> None:
    """Optional fields get sensible defaults."""
    job = make_job(
        description="",
        salary_min=None,
        salary_max=None,
        salary_currency="USD",
        location="",
        employment_type=None,
        experience_level=None,
        posted_date=None,
    )

    assert job.description == ""
    assert job.salary_min is None
    assert job.salary_max is None
    assert job.salary_currency == "USD"
    assert job.location == ""
    assert job.employment_type is None
    assert job.experience_level is None
    assert job.posted_date is None
    assert job.created_at is not None
    assert job.updated_at is not None


def test_timestamps_are_utc() -> None:
    """created_at and updated_at are timezone-aware UTC datetimes."""
    job = make_job()

    assert job.created_at.tzinfo is not None
    assert job.updated_at.tzinfo is not None


def test_currency_normalized_to_uppercase() -> None:
    """Currency codes are normalized to uppercase."""
    job = make_job(salary_currency="vnd")

    assert job.salary_currency == "VND"


def test_salary_max_below_min_rejected() -> None:
    """salary_max below salary_min raises a validation error."""
    with pytest.raises(ValidationError):
        make_job(salary_min=80000.0, salary_max=50000.0)


def test_salary_max_equal_to_min_accepted() -> None:
    """salary_max equal to salary_min is valid."""
    job = make_job(salary_min=50000.0, salary_max=50000.0)

    assert job.salary_min == job.salary_max == 50000.0


def test_empty_title_rejected() -> None:
    """An empty title raises a validation error."""
    with pytest.raises(ValidationError):
        make_job(title="")


def test_invalid_url_rejected() -> None:
    """An invalid URL raises a validation error."""
    with pytest.raises(ValidationError):
        make_job(url="not-a-url")