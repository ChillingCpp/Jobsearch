"""Tests for the configuration loading layer."""

import pytest
from pydantic import ValidationError

from src.core.config import load_all_configs, load_config


def test_load_valid_config() -> None:
    """A valid YAML config is loaded into a WebsiteConfig."""
    config = load_config("configs/example.yaml")

    assert config.name == "example_site"
    assert str(config.start_url) == "https://example.com/jobs"
    assert config.selectors["title"] == ".job-title"
    assert config.pagination is not None
    assert config.pagination.next_selector == ".pagination-next"
    assert config.pagination.max_pages == 5
    assert len(config.browser_actions) == 1
    assert config.browser_actions[0].action == "wait_for_selector"
    assert config.request_headers["User-Agent"] is not None


def test_load_missing_file_raises(tmp_path) -> None:
    """Loading a non-existent file raises FileNotFoundError."""
    missing = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(missing)


def test_load_invalid_config_raises(tmp_path) -> None:
    """An invalid YAML config raises a validation error."""
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text(
        "name: ''\n"
        "start_url: 'not-a-url'\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_config(invalid)


def test_load_all_configs(tmp_path) -> None:
    """All YAML files in a directory are loaded."""
    (tmp_path / "site_a.yaml").write_text(
        "name: site_a\nstart_url: https://a.example.com/jobs\n",
        encoding="utf-8",
    )
    (tmp_path / "site_b.yml").write_text(
        "name: site_b\nstart_url: https://b.example.com/jobs\n",
        encoding="utf-8",
    )

    configs = load_all_configs(tmp_path)

    assert len(configs) == 2
    names = {config.name for config in configs}
    assert names == {"site_a", "site_b"}