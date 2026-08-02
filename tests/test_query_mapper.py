"""Tests for the QueryMapper."""

from src.core.query_mapper import QueryMapper

SAMPLE_MAPPINGS = {
    "it": ["backend", "frontend", "fullstack", "software engineer", "devops"],
    "marketing": ["marketing", "digital marketing", "content marketing"],
    "sales": ["sales", "kinh doanh", "business development"],
}


def test_known_category_maps_to_keywords() -> None:
    """A known category maps to multiple search keywords."""
    mapper = QueryMapper(SAMPLE_MAPPINGS)

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
    mapper = QueryMapper(SAMPLE_MAPPINGS)

    keywords = mapper.map("data science")

    assert keywords == ["data science"]


def test_empty_mappings_returns_category_itself() -> None:
    """With no mappings, any category returns itself."""
    mapper = QueryMapper()

    assert mapper.map("it") == ["it"]
    assert mapper.map("anything") == ["anything"]


def test_category_is_case_insensitive() -> None:
    """Category matching is case-insensitive."""
    mapper = QueryMapper(SAMPLE_MAPPINGS)

    assert mapper.map("IT") == mapper.map("it")
    assert mapper.map("Marketing") == mapper.map("marketing")


def test_category_whitespace_is_trimmed() -> None:
    """Category whitespace is trimmed before matching."""
    mapper = QueryMapper(SAMPLE_MAPPINGS)

    assert mapper.map("  it  ") == mapper.map("it")


def test_add_mapping_is_extensible() -> None:
    """New mappings can be added at runtime."""
    mapper = QueryMapper(SAMPLE_MAPPINGS)
    mapper.add_mapping("finance", ["accountant", "financial analyst"])

    assert mapper.map("finance") == ["accountant", "financial analyst"]