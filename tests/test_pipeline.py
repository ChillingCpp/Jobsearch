"""Tests for the job aggregation pipeline."""

from unittest.mock import Mock

import pytest

from src.core.config import WebsiteConfig
from src.core.pipeline import run_pipeline
from src.database.models import Base
from src.database.session import create_engine, create_session
from src.normalizer.normalizer import Normalizer
from src.parser.extractor import Parser
from src.storage.repository import JobRepository

SAMPLE_HTML = """
<html>
<body>
  <div class="job-listing">
    <a class="job-link" href="https://example.com/jobs/1">Engineer</a>
    <div class="job-title">Engineer</div>
    <div class="job-company">Acme</div>
    <div class="job-location">Hanoi</div>
  </div>
</body>
</html>
"""


def make_config() -> WebsiteConfig:
    """Create a test website config."""
    return WebsiteConfig(
        name="test_site",
        start_url="https://example.com/jobs",
        selectors={
            "job_listing": ".job-listing",
            "title": ".job-title",
            "company": ".job-company",
            "description": ".job-description",
            "url": "a.job-link",
            "salary": ".job-salary",
            "location": ".job-location",
            "posted_date": ".job-date",
        },
    )


@pytest.fixture()
def session():
    """Create an in-memory SQLite session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = create_session(engine)
    test_session = session_factory()
    yield test_session
    test_session.close()


def test_pipeline_processes_config(session) -> None:
    """The pipeline fetches, parses, normalizes, and stores jobs."""
    fetcher = Mock()
    fetcher.fetch.return_value = SAMPLE_HTML

    repository = JobRepository(session)
    stored = run_pipeline(
        [make_config()],
        fetcher,
        Parser(),
        Normalizer(),
        repository,
    )

    assert stored == 1
    records = repository.find_all()
    assert len(records) == 1
    assert records[0].title == "Engineer"
    assert records[0].company == "Acme"
    assert records[0].source == "test_site"


def test_pipeline_handles_fetch_failure(session) -> None:
    """The pipeline continues when a fetch fails."""
    fetcher = Mock()
    fetcher.fetch.side_effect = Exception("network error")

    repository = JobRepository(session)
    stored = run_pipeline(
        [make_config()],
        fetcher,
        Parser(),
        Normalizer(),
        repository,
    )

    assert stored == 0
    assert repository.find_all() == []


def test_pipeline_handles_no_jobs(session) -> None:
    """The pipeline handles a config with no job listings gracefully."""
    fetcher = Mock()
    fetcher.fetch.return_value = "<html><body><p>No jobs</p></body></html>"

    repository = JobRepository(session)
    stored = run_pipeline(
        [make_config()],
        fetcher,
        Parser(),
        Normalizer(),
        repository,
    )

    assert stored == 0
    assert repository.find_all() == []