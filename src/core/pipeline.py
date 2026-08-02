"""Job aggregation pipeline."""

import logging
from urllib.parse import quote

from pydantic import ValidationError

from src.core.config import WebsiteConfig
from src.core.query_mapper import QueryMapper
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
    query_mapper: QueryMapper | None = None,
    category: str | None = None,
) -> int:
    """Run the full pipeline for all website configs.

    Args:
        configs: List of website configurations.
        fetcher: The HTML fetcher.
        parser: The HTML parser.
        normalizer: The value normalizer.
        repository: The job repository.
        query_mapper: Optional QueryMapper for keyword-based searching.
        category: Optional logical job category to map to search keywords.

    Returns:
        The total number of jobs stored.
    """
    total_stored = 0

    for config in configs:
        logger.info("Processing config: %s", config.name)
        total_stored += _process_config(
            config, fetcher, parser, normalizer, repository, query_mapper, category
        )

    logger.info("Pipeline complete. Stored %d jobs.", total_stored)
    return total_stored


def _process_config(
    config: WebsiteConfig,
    fetcher: Fetcher,
    parser: Parser,
    normalizer: Normalizer,
    repository: JobRepository,
    query_mapper: QueryMapper | None = None,
    category: str | None = None,
) -> int:
    """Process a single website config, including pagination.

    Args:
        config: The website configuration.
        fetcher: The HTML fetcher.
        parser: The HTML parser.
        normalizer: The value normalizer.
        repository: The job repository.
        query_mapper: Optional QueryMapper for keyword-based searching.
        category: Optional logical job category to map to search keywords.

    Returns:
        The number of jobs stored for this config.
    """
    stored = 0
    max_pages = config.pagination.max_pages if config.pagination else 1
    page_param = config.pagination.page_param if config.pagination else None
    actions = [action.model_dump() for action in config.browser_actions] if config.browser_actions else None

    # Determine the list of URLs to scrape.
    # If a search_url and category are provided, map the category to keywords
    # and build one search URL per keyword.
    urls = _build_search_urls(config, query_mapper, category)

    for url in urls:
        stored += _scrape_url(
            config, url, fetcher, parser, normalizer, repository,
            max_pages, page_param, actions,
        )

    return stored


def _build_search_urls(
    config: WebsiteConfig,
    query_mapper: QueryMapper | None,
    category: str | None,
) -> list[str]:
    """Build the list of URLs to scrape for a config.

    If a search_url and category are provided, the category is mapped to
    keywords and one search URL is built per keyword. Otherwise, the
    config's start_url is used as-is.

    Args:
        config: The website configuration.
        query_mapper: Optional QueryMapper for keyword-based searching.
        category: Optional logical job category to map to search keywords.

    Returns:
        A list of URLs to scrape.
    """
    if config.search_url is not None and query_mapper is not None and category:
        keywords = query_mapper.map(category)
        logger.info("Mapped category '%s' to keywords: %s", category, keywords)
        return [_build_keyword_url(str(config.search_url), keyword) for keyword in keywords]

    return [str(config.start_url)]


def _build_keyword_url(search_url: str, keyword: str) -> str:
    """Build a search URL with a keyword.

    The keyword is URL-encoded and inserted into the search URL.
    The search URL should contain a placeholder `{keyword}`.

    Args:
        search_url: The search URL template with a `{keyword}` placeholder.
        keyword: The search keyword.

    Returns:
        The search URL with the keyword substituted.
    """
    encoded = quote(keyword)
    return search_url.replace("{keyword}", encoded)


def _scrape_url(
    config: WebsiteConfig,
    url: str,
    fetcher: Fetcher,
    parser: Parser,
    normalizer: Normalizer,
    repository: JobRepository,
    max_pages: int,
    page_param: str | None,
    actions: list[dict] | None,
) -> int:
    """Scrape a single URL across paginated pages.

    Args:
        config: The website configuration.
        url: The base URL to scrape.
        fetcher: The HTML fetcher.
        parser: The HTML parser.
        normalizer: The value normalizer.
        repository: The job repository.
        max_pages: Maximum number of pages to scrape.
        page_param: The pagination query parameter name.
        actions: Optional browser actions.

    Returns:
        The number of jobs stored for this URL.
    """
    stored = 0

    for page_num in range(1, max_pages + 1):
        page_url = _build_page_url(url, page_param, page_num)
        logger.info("Fetching %s page %d: %s", config.name, page_num, page_url)

        try:
            if actions:
                html = fetcher.fetch_with_browser(page_url, actions=actions)
            else:
                html = fetcher.fetch(page_url, headers=config.request_headers)
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