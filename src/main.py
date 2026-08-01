"""Job aggregator CLI entry point."""

import argparse
import logging

from src.core.config import load_all_configs
from src.core.pipeline import run_pipeline
from src.crawler.fetcher import Fetcher
from src.database.models import Base
from src.database.session import create_engine, create_session
from src.normalizer.normalizer import Normalizer
from src.parser.extractor import Parser
from src.scheduler.scheduler import Scheduler
from src.storage.repository import JobRepository

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(description="Job aggregator")
    parser.add_argument(
        "--configs",
        default="configs/",
        help="Path to the configs directory (default: configs/)",
    )
    parser.add_argument(
        "--database",
        default="sqlite:///jobs.db",
        help="Database URL (default: sqlite:///jobs.db)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the pipeline once",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Run the pipeline repeatedly at the given interval in seconds",
    )
    return parser


def main() -> None:
    """Run the job aggregation pipeline."""
    args = build_parser().parse_args()

    configs = load_all_configs(args.configs)
    if not configs:
        logger.warning("No configs found in %s", args.configs)
        return

    engine = create_engine(args.database)
    Base.metadata.create_all(engine)
    session_factory = create_session(engine)

    fetcher = Fetcher()
    parser = Parser()
    normalizer = Normalizer()

    def job() -> None:
        with session_factory() as session:
            repository = JobRepository(session)
            run_pipeline(configs, fetcher, parser, normalizer, repository)

    scheduler = Scheduler(job)

    if args.once:
        scheduler.run_once()
    elif args.interval > 0:
        logger.info("Running pipeline every %d seconds", args.interval)
        scheduler.run_every(args.interval)
    else:
        scheduler.run_once()


if __name__ == "__main__":
    main()