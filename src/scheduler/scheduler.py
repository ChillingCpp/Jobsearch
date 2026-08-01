"""Simple scheduler for triggering the crawl pipeline."""

import threading
from typing import Callable


class Scheduler:
    """Runs a job function once or at regular intervals."""

    def __init__(self, job_function: Callable[[], None]) -> None:
        """Initialize the scheduler with a job function.

        Args:
            job_function: The callable that runs the crawl pipeline.
        """
        self.job_function = job_function
        self._stop_event = threading.Event()

    def run_once(self) -> None:
        """Run the job function once (manual crawl)."""
        self.job_function()

    def run_every(self, interval_seconds: int) -> None:
        """Run the job function repeatedly at the given interval.

        Args:
            interval_seconds: Seconds between each run.
        """
        self._stop_event.clear()
        while not self._stop_event.is_set():
            self.job_function()
            self._stop_event.wait(interval_seconds)

    def stop(self) -> None:
        """Stop the scheduled execution."""
        self._stop_event.set()