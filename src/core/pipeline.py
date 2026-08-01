"""Job aggregation pipeline."""

import logging

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
        try:
            html = fetcher.fetch(str(config.start_url), headers=config.request_headers)
        except Exception as error:
            logger.error("Failed to fetch %s: %s", config.name, error)
            continue

        raw_jobs = parser.parse(html, config)
        logger.info("Parsed %d raw jobs from %s", len(raw_jobs), config.name)

        for raw_job in raw_jobs:
            job = normalizer.normalize(raw_job, config.name)
            repository.upsert(job)
            total_stored += 1

    logger.info("Pipeline complete. Stored %d jobs.", total_stored)
    return total_stored