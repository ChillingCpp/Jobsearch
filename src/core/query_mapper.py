"""QueryMapper maps logical job categories to search keywords."""

from __future__ import annotations


class QueryMapper:
    """Maps a logical job category into one or more search keywords.

    The mapper is intentionally simple: it only maps categories to keywords.
    It does not perform any scraping, parsing, or filtering logic.

    Mappings are provided via configuration, not hardcoded.
    """

    def __init__(self, mappings: dict[str, list[str]] | None = None) -> None:
        """Initialize the mapper with category-to-keywords mappings.

        Args:
            mappings: Category-to-keywords mappings from configuration.
                If None, no mappings are known and all categories return
                themselves as a single keyword.
        """
        self._mappings: dict[str, list[str]] = {}
        if mappings:
            for category, keywords in mappings.items():
                self._mappings[category.strip().lower()] = keywords

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