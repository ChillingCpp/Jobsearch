"""Tests for the HTML parser."""

from src.core.config import WebsiteConfig
from src.parser.extractor import Parser


def make_config(**overrides) -> WebsiteConfig:
    """Create a WebsiteConfig with test selectors."""
    defaults = {
        "name": "test_site",
        "start_url": "https://example.com/jobs",
        "selectors": {
            "job_listing": ".job-listing",
            "title": ".job-title",
            "company": ".job-company",
            "description": ".job-description",
            "url": "a.job-link",
            "salary": ".job-salary",
            "location": ".job-location",
            "posted_date": ".job-date",
        },
    }
    defaults.update(overrides)
    return WebsiteConfig(**defaults)


SINGLE_JOB_HTML = """
<html>
<body>
  <div class="job-listing">
    <a class="job-link" href="/jobs/1">Software Engineer</a>
    <div class="job-title">Software Engineer</div>
    <div class="job-company">Acme Corp</div>
    <div class="job-description">Build cool stuff.</div>
    <div class="job-salary">$50,000 - $80,000</div>
    <div class="job-location">Ho Chi Minh City</div>
    <div class="job-date">2026-01-01</div>
  </div>
</body>
</html>
"""

MULTI_JOB_HTML = """
<html>
<body>
  <div class="job-listing">
    <a class="job-link" href="/jobs/1">Engineer</a>
    <div class="job-title">Engineer</div>
    <div class="job-company">Acme</div>
    <div class="job-location">Hanoi</div>
  </div>
  <div class="job-listing">
    <a class="job-link" href="/jobs/2">Designer</a>
    <div class="job-title">Designer</div>
    <div class="job-company">Beta</div>
    <div class="job-location">Da Nang</div>
  </div>
</body>
</html>
"""

MISSING_FIELDS_HTML = """
<html>
<body>
  <div class="job-listing">
    <div class="job-title">Only Title</div>
  </div>
</body>
</html>
"""

NO_JOBS_HTML = """
<html>
<body>
  <p>No jobs available.</p>
</body>
</html>
"""


def test_parse_single_job() -> None:
    """A single job listing is parsed correctly."""
    parser = Parser()
    config = make_config()

    jobs = parser.parse(SINGLE_JOB_HTML, config)

    assert len(jobs) == 1
    job = jobs[0]
    assert job.title == "Software Engineer"
    assert job.company == "Acme Corp"
    assert job.description == "Build cool stuff."
    assert job.url == "/jobs/1"
    assert job.salary == "$50,000 - $80,000"
    assert job.location == "Ho Chi Minh City"
    assert job.posted_date == "2026-01-01"


def test_parse_multiple_jobs() -> None:
    """Multiple job listings are parsed into multiple RawJobs."""
    parser = Parser()
    config = make_config()

    jobs = parser.parse(MULTI_JOB_HTML, config)

    assert len(jobs) == 2
    assert jobs[0].title == "Engineer"
    assert jobs[0].company == "Acme"
    assert jobs[1].title == "Designer"
    assert jobs[1].company == "Beta"


def test_parse_missing_fields_are_empty() -> None:
    """Missing fields become empty strings, not errors."""
    parser = Parser()
    config = make_config()

    jobs = parser.parse(MISSING_FIELDS_HTML, config)

    assert len(jobs) == 1
    job = jobs[0]
    assert job.title == "Only Title"
    assert job.company == ""
    assert job.description == ""
    assert job.url == ""
    assert job.salary == ""
    assert job.location == ""
    assert job.posted_date == ""


def test_parse_no_jobs_returns_empty() -> None:
    """A page with no job listings returns an empty list."""
    parser = Parser()
    config = make_config()

    jobs = parser.parse(NO_JOBS_HTML, config)

    assert jobs == []


def test_parse_without_listing_selector_returns_empty() -> None:
    """A config without a job_listing selector returns an empty list."""
    parser = Parser()
    config = make_config(selectors={"title": ".job-title"})

    jobs = parser.parse(SINGLE_JOB_HTML, config)

    assert jobs == []