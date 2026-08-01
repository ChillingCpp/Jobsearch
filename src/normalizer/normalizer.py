"""Normalizer that converts raw job data into standardized Job records."""

import re
from datetime import datetime

from src.models.job import Job
from src.parser.extractor import RawJob

_NEGOTIABLE_TERMS = {"thỏa thuận", "negotiable", "thương lượng", "tt"}
_CURRENCY_SYMBOLS = "$€£₫"
_CURRENCY_WORDS = ["usd", "vnd", "eur", "gbp", "triệu", "tr", "k", "đ"]

# Currency mapping
_CURRENCY_MAP = {
    "$": "USD",
    "usd": "USD",
    "đ": "VND",
    "vnd": "VND",
    "triệu": "VND",
    "tr": "VND",
    "k": "VND",
    "€": "EUR",
    "eur": "EUR",
    "£": "GBP",
    "gbp": "GBP",
}

# Employment type mapping
_EMPLOYMENT_TYPE_MAP = {
    "full time": "full_time",
    "full-time": "full_time",
    "toàn thời gian": "full_time",
    "part time": "part_time",
    "part-time": "part_time",
    "bán thời gian": "part_time",
    "contract": "contract",
    "hợp đồng": "contract",
    "internship": "internship",
    "thực tập": "internship",
    "remote": "remote",
    "từ xa": "remote",
}

# Experience level mapping
_EXPERIENCE_LEVEL_MAP = {
    "entry": "entry",
    "entry level": "entry",
    "mới tốt nghiệp": "entry",
    "junior": "junior",
    "1 năm": "junior",
    "mid": "mid",
    "middle": "mid",
    "2 năm": "mid",
    "senior": "senior",
    "3 năm": "senior",
    "lead": "lead",
    "manager": "manager",
    "quản lý": "manager",
}

# Date formats
_DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%d %b %Y",
    "%b %d, %Y",
    "%d/%m/%y",
]


class Normalizer:
    """Converts raw job data into standardized Job records."""

    def normalize(self, raw: RawJob, source: str) -> Job:
        """Normalize a RawJob into a validated Job.

        Args:
            raw: The raw job data from the parser.
            source: The website name (used as the job source).

        Returns:
            A validated Job.
        """
        salary_min, salary_max, salary_currency = self._parse_salary(raw.salary)

        return Job(
            title=raw.title,
            company=raw.company,
            description=raw.description,
            url=raw.url,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_currency=salary_currency,
            location=raw.location.strip(),
            employment_type=self._map_employment_type(raw.title + " " + raw.description),
            experience_level=self._map_experience_level(raw.title + " " + raw.description),
            posted_date=self._parse_date(raw.posted_date),
            source=source,
            source_id=raw.url,
        )

    @staticmethod
    def _parse_salary(text: str) -> tuple[float | None, float | None, str]:
        """Parse a salary string into (min, max, currency)."""
        if not text:
            return None, None, "USD"

        cleaned = text.strip().lower()
        if cleaned in _NEGOTIABLE_TERMS:
            return None, None, "USD"

        # Detect currency
        currency = "USD"
        for symbol, code in _CURRENCY_MAP.items():
            if symbol in cleaned:
                currency = code
                break

        # Remove currency symbols and words
        cleaned = re.sub(f"[{_CURRENCY_SYMBOLS}]", "", cleaned)
        for word in _CURRENCY_WORDS:
            cleaned = cleaned.replace(word, "")

        # Try range: "50,000 - 80,000"
        range_match = re.match(r"\s*([\d.,]+)\s*[-–—]\s*([\d.,]+)\s*$", cleaned)
        if range_match:
            min_val = float(range_match.group(1).replace(",", ""))
            max_val = float(range_match.group(2).replace(",", ""))
            return min_val, max_val, currency

        # Try single: "1000"
        single_match = re.match(r"\s*([\d.,]+)\s*$", cleaned)
        if single_match:
            amount = float(single_match.group(1).replace(",", ""))
            return amount, amount, currency

        return None, None, "USD"

    @staticmethod
    def _map_employment_type(text: str) -> str | None:
        """Map a raw employment type string to a standard value."""
        lowered = text.lower()
        for key, value in _EMPLOYMENT_TYPE_MAP.items():
            if key in lowered:
                return value
        return None

    @staticmethod
    def _map_experience_level(text: str) -> str | None:
        """Map a raw experience level string to a standard value."""
        lowered = text.lower()
        for key, value in _EXPERIENCE_LEVEL_MAP.items():
            if key in lowered:
                return value
        return None

    @staticmethod
    def _parse_date(text: str) -> datetime | None:
        """Parse a date string into a datetime, or None if unparseable."""
        if not text:
            return None

        cleaned = text.strip()
        for fmt in _DATE_FORMATS:
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue
        return None