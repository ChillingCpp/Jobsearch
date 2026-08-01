"""Tests for the scheduler."""

import threading
import time

from src.scheduler.scheduler import Scheduler


def test_run_once_calls_job_once() -> None:
    """run_once calls the job function exactly once."""
    calls = []

    def job() -> None:
        calls.append("run")

    scheduler = Scheduler(job)
    scheduler.run_once()

    assert len(calls) == 1


def test_run_every_calls_job_multiple_times() -> None:
    """run_every calls the job function repeatedly at the interval."""
    calls = []

    def job() -> None:
        calls.append("run")

    scheduler = Scheduler(job)

    thread = threading.Thread(target=scheduler.run_every, args=(0.05,))
    thread.start()
    time.sleep(0.15)
    scheduler.stop()
    thread.join(timeout=2)

    assert len(calls) >= 2


def test_stop_halts_execution() -> None:
    """stop halts the scheduled execution."""
    calls = []

    def job() -> None:
        calls.append("run")

    scheduler = Scheduler(job)

    thread = threading.Thread(target=scheduler.run_every, args=(0.01,))
    thread.start()
    time.sleep(0.05)
    scheduler.stop()
    thread.join(timeout=2)

    count_after_stop = len(calls)
    time.sleep(0.05)

    assert len(calls) == count_after_stop