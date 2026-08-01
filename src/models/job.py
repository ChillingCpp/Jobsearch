"""Normalized job data model."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field, HttpUrl, field_validator


def _utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


class Job(BaseModel):
    """A normalized job posting independent of any source website."""

    title: str = Field(min_length=1)
    company: str = Field(min_length=1)
    description: str = ""
    url: HttpUrl
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str = "USD"
    location: str = ""
    employment_type: str | None = None
    experience_level: str | None = None
    posted_date: datetime | None = None
    source: str
    source_id: str
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("salary_max")
    @classmethod
    def salary_max_not_below_min(cls, value: float | None, info) -> float | None:
        """Ensure salary_max is not below salary_min."""
        salary_min = info.data.get("salary_min")
        if (
            value is not None
            and salary_min is not None
            and value < salary_min
        ):
            raise ValueError("salary_max must be greater than or equal to salary_min")
        return value

    @field_validator("salary_currency")
    @classmethod
    def currency_is_uppercase(cls, value: str) -> str:
        """Normalize currency code to uppercase."""
        return value.upper()