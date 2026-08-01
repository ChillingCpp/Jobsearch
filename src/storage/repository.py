"""Job repository for storing and querying job records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import JobRecord
from src.models.job import Job


class JobRepository:
    """Provides CRUD operations for job records."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a database session."""
        self.session = session

    def save(self, job: Job) -> JobRecord:
        """Insert a new job record.

        Args:
            job: The normalized job to store.

        Returns:
            The saved JobRecord.
        """
        record = self._to_record(job)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def upsert(self, job: Job) -> JobRecord:
        """Update an existing record by (source, source_id) or insert a new one.

        Args:
            job: The normalized job to store.

        Returns:
            The saved or updated JobRecord.
        """
        existing = self.find_by_source_id(job.source, job.source_id)
        if existing is not None:
            self._update_record(existing, job)
            self.session.commit()
            self.session.refresh(existing)
            return existing
        return self.save(job)

    def find_by_source_id(self, source: str, source_id: str) -> JobRecord | None:
        """Find a record by source and source_id.

        Args:
            source: The website name.
            source_id: The unique ID on the source website.

        Returns:
            The matching JobRecord, or None if not found.
        """
        stmt = select(JobRecord).where(
            JobRecord.source == source,
            JobRecord.source_id == source_id,
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def find_all(self) -> list[JobRecord]:
        """Return all job records.

        Returns:
            A list of all JobRecords.
        """
        stmt = select(JobRecord).order_by(JobRecord.created_at.desc())
        return list(self.session.execute(stmt).scalars().all())

    @staticmethod
    def _to_record(job: Job) -> JobRecord:
        """Convert a Job model to a JobRecord."""
        return JobRecord(
            title=job.title,
            company=job.company,
            description=job.description,
            url=str(job.url),
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            salary_currency=job.salary_currency,
            location=job.location,
            employment_type=job.employment_type,
            experience_level=job.experience_level,
            posted_date=job.posted_date,
            source=job.source,
            source_id=job.source_id,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )

    @staticmethod
    def _update_record(record: JobRecord, job: Job) -> None:
        """Update an existing JobRecord from a Job model."""
        record.title = job.title
        record.company = job.company
        record.description = job.description
        record.url = str(job.url)
        record.salary_min = job.salary_min
        record.salary_max = job.salary_max
        record.salary_currency = job.salary_currency
        record.location = job.location
        record.employment_type = job.employment_type
        record.experience_level = job.experience_level
        record.posted_date = job.posted_date
        record.updated_at = job.updated_at