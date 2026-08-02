"""Tests for the job aggregation pipeline."""

from unittest.mock import Mock

import pytest

from src.core.config import WebsiteConfig
from src.core.pipeline import run_pipeline
from src.core.query_mapper import QueryMapper
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


INVALID_JOB_HTML = """
<html>
<body>
  <div class="job-listing">
    <div class="job-title"></div>
    <div class="job-company"></div>
  </div>
</body>
</html>
"""


def test_pipeline_skips_invalid_jobs(session) -> None:
    """The pipeline skips jobs with missing required fields."""
    fetcher = Mock()
    fetcher.fetch.return_value = INVALID_JOB_HTML

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


def test_pipeline_uses_config_category_mappings(session) -> None:
    """The pipeline uses config's category_mappings to build search URLs."""
    fetcher = Mock()
    fetcher.fetch.return_value = SAMPLE_HTML

    config = make_config()
    config.search_url = "https://example.com/search?q={keyword}"
    config.category_mappings = {
        "it": ["backend", "frontend", "fullstack", "software engineer", "devops"],
    }

    repository = JobRepository(session)
    stored = run_pipeline(
        [config],
        fetcher,
        Parser(),
        Normalizer(),
        repository,
        category="it",
    )

    assert stored == 5  # 5 keywords for "it" category
    assert fetcher.fetch.call_count == 5

    # Verify the URLs used the mapped keywords
    urls = [call.args[0] for call in fetcher.fetch.call_args_list]
    assert "https://example.com/search?q=backend" in urls
    assert "https://example.com/search?q=frontend" in urls
    assert "https://example.com/search?q=fullstack" in urls
    assert "https://example.com/search?q=software%20engineer" in urls
    assert "https://example.com/search?q=devops" in urls


def test_pipeline_uses_global_query_mapper_when_no_config_mappings(session) -> None:
    """The pipeline falls back to global query_mapper when config has no mappings."""
    fetcher = Mock()
    fetcher.fetch.return_value = SAMPLE_HTML

    config = make_config()
    config.search_url = "https://example.com/search?q={keyword}"

    global_mapper = QueryMapper(
        {"it": ["backend", "frontend"]}
    )

    repository = JobRepository(session)
    stored = run_pipeline(
        [config],
        fetcher,
        Parser(),
        Normalizer(),
        repository,
        query_mapper=global_mapper,
        category="it",
    )

    assert stored == 2  # 2 keywords from global mapper
    assert fetcher.fetch.call_count == 2
