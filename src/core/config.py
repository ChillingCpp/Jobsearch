"""Configuration loading for website definitions."""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, HttpUrl


class Pagination(BaseModel):
    """Rules for navigating paginated job listings."""

    next_selector: str
    max_pages: int | None = None
    page_param: str | None = None


class BrowserAction(BaseModel):
    """A single browser action to perform before extraction."""

    action: str
    selector: str | None = None
    value: str | None = None


class WebsiteConfig(BaseModel):
    """Configuration describing how to crawl and parse one website."""

    name: str = Field(min_length=1)
    start_url: HttpUrl
    search_url: HttpUrl | None = None
    selectors: dict[str, str] = Field(default_factory=dict)
    pagination: Pagination | None = None
    browser_actions: list[BrowserAction] = Field(default_factory=list)
    request_headers: dict[str, str] = Field(default_factory=dict)
    category_mappings: dict[str, list[str]] = Field(default_factory=dict)


def load_config(path: str | Path) -> WebsiteConfig:
    """Load and validate a single website configuration from YAML."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return WebsiteConfig(**data)


def load_all_configs(config_dir: str | Path) -> list[WebsiteConfig]:
    """Load every YAML configuration file in a directory."""
    directory = Path(config_dir)
    configs: list[WebsiteConfig] = []
    for file_path in sorted(directory.glob("*.yaml")) + sorted(directory.glob("*.yml")):
        configs.append(load_config(file_path))
    return configs