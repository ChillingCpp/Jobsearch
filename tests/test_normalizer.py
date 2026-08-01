"""Tests for the normalizer."""

from datetime import datetime

from src.normalizer.normalizer import Normalizer
from src.parser.extractor import RawJob


def make_raw_job(**overrides) -> RawJob:
    """Create a RawJob with test defaults."""
    defaults = {
        "title": "Software Engineer",
        "company": "Acme Corp",
        "description": "Full time position for senior developers.",
        "url": "https://example.com/jobs/123",
        "salary": "$50,000 - $80,000",
        "location": "  Ho Chi Minh City  ",
        "posted_date": "2026-01-15",
    }
    defaults.update(overrides)
    return RawJob(**defaults)


def test_salary_range_usd() -> None:
    """A USD salary range is parsed into min, max, and currency."""
    normalizer = Normalizer()
    raw = make_raw_job(salary="$50,000 - $80,000")

    job = normalizer.normalize(raw, "example_site")

    assert job.salary_min == 50000.0
    assert job.salary_max == 80000.0
    assert job.salary_currency == "USD"


def test_salary_range_vnd() -> None:
    """A VND salary range with 'triệu' is parsed correctly."""
    normalizer = Normalizer()
    raw = make_raw_job(salary="50 - 80 triệu")

    job = normalizer.normalize(raw, "example_site")

    assert job.salary_min == 50.0
    assert job.salary_max == 80.0
    assert job.salary_currency == "VND"


def test_salary_single_value() -> None:
    """A single salary value is parsed into min and max."""
    normalizer = Normalizer()
    raw = make_raw_job(salary="1000 USD")

    job = normalizer.normalize(raw, "example_site")

    assert job.salary_min == 1000.0
    assert job.salary_max == 1000.0
    assert job.salary_currency == "USD"


def test_salary_negotiable() -> None:
    """A negotiable salary results in None values."""
    normalizer = Normalizer()
    raw = make_raw_job(salary="Thỏa thuận")

    job = normalizer.normalize(raw, "example_site")

    assert job.salary_min is None
    assert job.salary_max is None


def test_salary_empty() -> None:
    """An empty salary results in None values."""
    normalizer = Normalizer()
    raw = make_raw_job(salary="")

    job = normalizer.normalize(raw, "example_site")

    assert job.salary_min is None
    assert job.salary_max is None


def test_employment_type_full_time() -> None:
    """Full time is mapped to the standard value."""
    normalizer = Normalizer()
    raw = make_raw_job(description="Full time position")

    job = normalizer.normalize(raw, "example_site")

    assert job.employment_type == "full_time"


def test_employment_type_remote() -> None:
    """Remote is mapped to the standard value."""
    normalizer = Normalizer()
    raw = make_raw_job(description="Remote work available")

    job = normalizer.normalize(raw, "example_site")

    assert job.employment_type == "remote"


def test_employment_type_unknown() -> None:
    """Unknown employment type results in None."""
    normalizer = Normalizer()
    raw = make_raw_job(description="Some vague description")

    job = normalizer.normalize(raw, "example_site")

    assert job.employment_type is None


def test_experience_level_senior() -> None:
    """Senior is mapped to the standard value."""
    normalizer = Normalizer()
    raw = make_raw_job(title="Senior Software Engineer")

    job = normalizer.normalize(raw, "example_site")

    assert job.experience_level == "senior"


def test_experience_level_entry() -> None:
    """Entry level is mapped to the standard value."""
    normalizer = Normalizer()
    raw = make_raw_job(description="Entry level position for new graduates")

    job = normalizer.normalize(raw, "example_site")

    assert job.experience_level == "entry"


def test_experience_level_unknown() -> None:
    """Unknown experience level results in None."""
    normalizer = Normalizer()
    raw = make_raw_job(title="Software Engineer", description="No experience info")

    job = normalizer.normalize(raw, "example_site")

    assert job.experience_level is None


def test_parse_date_iso() -> None:
    """ISO date format is parsed."""
    normalizer = Normalizer()
    raw = make_raw_job(posted_date="2026-01-15")

    job = normalizer.normalize(raw, "example_site")

    assert job.posted_date == datetime(2026, 1, 15)


def test_parse_date_dmy() -> None:
    """DD/MM/YYYY date format is parsed."""
    normalizer = Normalizer()
    raw = make_raw_job(posted_date="15/01/2026")

    job = normalizer.normalize(raw, "example_site")

    assert job.posted_date == datetime(2026, 1, 15)


def test_parse_date_invalid() -> None:
    """An unparseable date results in None."""
    normalizer = Normalizer()
    raw = make_raw_job(posted_date="yesterday")

    job = normalizer.normalize(raw, "example_site")

    assert job.posted_date is None


def test_full_normalization() -> None:
    """A complete RawJob is normalized into a valid Job."""
    normalizer = Normalizer()
    raw = make_raw_job()

    job = normalizer.normalize(raw, "example_site")

    assert job.title == "Software Engineer"
    assert job.company == "Acme Corp"
    assert job.description == "Full time position for senior developers."
    assert str(job.url) == "https://example.com/jobs/123"
    assert job.salary_min == 50000.0
    assert job.salary_max == 80000.0
    assert job.salary_currency == "USD"
    assert job.location == "Ho Chi Minh City"  # whitespace trimmed
    assert job.employment_type == "full_time"
    assert job.experience_level == "senior"
    assert job.posted_date == datetime(2026, 1, 15)
    assert job.source == "example_site"
    assert job.source_id == "https://example.com/jobs/123"