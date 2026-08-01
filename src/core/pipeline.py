"""Job aggregation pipeline."""

import logging

from pydantic import ValidationError

from src.core.config import WebsiteConfig
from src.crawler.fetcher import Fetcher
from src.normalizer.normalizer import Normalizer
from src.parser.extractor import Parser
from src.storage.repository import JobRepository

logger = logging.getLogger(__name__)


def run_pipeline(
    configs: list[WebsiteConfig],
    fetcher: Fetcher,
    parser: Parser,
    normalizer: Normalizer,
    repository: JobRepository,
) -> int:
    """Run the full pipeline for all website configs.

    Args:
        configs: List of website configurations.
        fetcher: The HTML fetcher.
        parser: The HTML parser.
        normalizer: The value normalizer.
        repository: The job repository.

    Returns:
        The total number of jobs stored.
    """
    total_stored = 0

    for config in configs:
        logger.info("Processing config: %s", config.name)
        total_stored += _process_config(config, fetcher, parser, normalizer, repository)

    logger.info("Pipeline complete. Stored %d jobs.", total_stored)
    return total_stored


def _process_config(
    config: WebsiteConfig,
    fetcher: Fetcher,
    parser: Parser,
    normalizer: Normalizer,
    repository: JobRepository,
) -> int:
    """Process a single website config, including pagination.

    Args:
        config: The website configuration.
        fetcher: The HTML fetcher.
        parser: The HTML parser.
        normalizer: The value normalizer.
        repository: The job repository.

    Returns:
        The number of jobs stored for this config.
    """
    stored = 0
    max_pages = config.pagination.max_pages if config.pagination else 1
    page_param = config.pagination.page_param if config.pagination else None
    actions = [action.model_dump() for action in config.browser_actions] if config.browser_actions else None

    for page_num in range(1, max_pages + 1):
        url = _build_page_url(str(config.start_url), page_param, page_num)
        logger.info("Fetching %s page %d: %s", config.name, page_num, url)

        try:
            if actions:
                html = fetcher.fetch_with_browser(url, actions=actions)
            else:
                html = fetcher.fetch(url, headers=config.request_headers)
        except Exception as error:
            logger.error("Failed to fetch %s page %d: %s", config.name, page_num, error)
            break

        raw_jobs = parser.parse(html, config)
        logger.info("Parsed %d raw jobs from %s page %d", len(raw_jobs), config.name, page_num)

        if not raw_jobs:
            logger.info("No more jobs on page %d, stopping.", page_num)
            break

        for raw_job in raw_jobs:
            try:
                job = normalizer.normalize(raw_job, config.name)
            except ValidationError as error:
                logger.warning("Skipping invalid job from %s: %s", config.name, error)
                continue
            repository.upsert(job)
            stored += 1

    return stored


def _build_page_url(base_url: str, page_param: str | None, page_num: int) -> str:
    """Build a URL for a specific page number.

    Args:
        base_url: The base URL.
        page_param: The query parameter name for pagination (e.g. "page").
        page_num: The page number (1-based).

    Returns:
        The URL for the given page.
    """
    if page_param is None or page_num == 1:
        return base_url

    separator = "&" if "?" in base_url else "?"
    return f"{base_url}{separator}{page_param}={page_num}"