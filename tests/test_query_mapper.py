"""Tests for the QueryMapper."""

from src.core.query_mapper import QueryMapper


def test_known_category_maps_to_keywords() -> None:
    """A known category maps to multiple search keywords."""
    mapper = QueryMapper()

    keywords = mapper.map("it")

    assert keywords == [
        "backend",
        "frontend",
        "fullstack",
        "software engineer",
        "devops",
    ]


def test_unknown_category_returns_itself() -> None:
    """An unknown category returns itself as a single keyword."""
    mapper = QueryMapper()

    keywords = mapper.map("data science")

    assert keywords == ["data science"]


def test_category_is_case_insensitive() -> None:
    """Category matching is case-insensitive."""
    mapper = QueryMapper()

    assert mapper.map("IT") == mapper.map("it")
    assert mapper.map("Marketing") == mapper.map("marketing")


def test_category_whitespace_is_trimmed() -> None:
    """Category whitespace is trimmed before matching."""
    mapper = QueryMapper()

    assert mapper.map("  it  ") == mapper.map("it")


def test_custom_mappings_are_merged() -> None:
    """Custom mappings are merged over the defaults."""
    mapper = QueryMapper(mappings={"design": ["ui", "ux", "graphic design"]})

    # Default mapping still works
    assert "backend" in mapper.map("it")
    # Custom mapping works
    assert mapper.map("design") == ["ui", "ux", "graphic design"]


def test_add_mapping_is_extensible() -> None:
    """New mappings can be added at runtime."""
    mapper = QueryMapper()
    mapper.add_mapping("finance", ["accountant", "financial analyst"])

    assert mapper.map("finance") == ["accountant", "financial analyst"]