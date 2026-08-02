"""QueryMapper maps logical job categories to search keywords."""

from __future__ import annotations

from typing import ClassVar


class QueryMapper:
    """Maps a logical job category into one or more search keywords.

    The mapper is intentionally simple: it only maps categories to keywords.
    It does not perform any scraping, parsing, or filtering logic.
    """

    _DEFAULT_MAPPINGS: ClassVar[dict[str, list[str]]] = {
        "it": [
            "backend",
            "frontend",
            "fullstack",
            "software engineer",
            "devops",
        ],
        "marketing": [
            "marketing",
            "digital marketing",
            "content marketing",
        ],
        "sales": [
            "sales",
            "kinh doanh",
            "business development",
        ],
    }

    def __init__(self, mappings: dict[str, list[str]] | None = None) -> None:
        """Initialize the mapper with optional custom mappings.

        Args:
            mappings: Optional custom category-to-keywords mappings.
                These are merged over the default mappings.
        """
        self._mappings = dict(self._DEFAULT_MAPPINGS)
        if mappings:
            self._mappings.update(mappings)

    def map(self, category: str) -> list[str]:
        """Map a logical job category to search keywords.

        Args:
            category: The logical job category (e.g. "it", "marketing").

        Returns:
            A list of search keywords. Unknown categories return
            the category itself as a single keyword.
        """
        normalized = category.strip().lower()
        return self._mappings.get(normalized, [category])

    def add_mapping(self, category: str, keywords: list[str]) -> None:
        """Add or replace a category mapping.

        Args:
            category: The logical job category.
            keywords: The search keywords for this category.
        """
        self._mappings[category.strip().lower()] = keywords