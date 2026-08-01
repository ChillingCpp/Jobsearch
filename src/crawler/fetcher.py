"""HTML fetcher with retry support."""

import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)


class FetchError(Exception):
    """Raised when a page cannot be fetched after all retries."""


class Fetcher:
    """Downloads HTML from URLs with retry and delay support."""

    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0) -> None:
        """Initialize the fetcher.

        Args:
            max_retries: Number of attempts before giving up.
            retry_delay: Seconds to wait between attempts.
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def fetch(self, url: str, headers: dict[str, str] | None = None) -> str:
        """Download HTML using requests.

        Args:
            url: The page URL to download.
            headers: Optional request headers.

        Returns:
            The page HTML as a string.

        Raises:
            FetchError: If the request fails after all retries.
        """
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as error:
                last_error = error
                logger.warning(
                    "Request failed (attempt %s/%s): %s",
                    attempt,
                    self.max_retries,
                    error,
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        raise FetchError(
            f"Failed to fetch {url} after {self.max_retries} attempts: {last_error}"
        )

    def fetch_with_browser(self, url: str, actions: list[dict[str, Any]] | None = None) -> str:
        """Download HTML using Playwright with optional browser actions.

        Args:
            url: The page URL to download.
            actions: Optional list of browser actions, each with:
                - action: e.g. "wait_for_selector"
                - selector: CSS selector
                - value: optional value

        Returns:
            The page HTML as a string.

        Raises:
            FetchError: If the browser cannot load the page after all retries.
        """
        from playwright.sync_api import sync_playwright

        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch()
                    page = browser.new_page()
                    page.goto(url, timeout=60000)

                    for action in actions or []:
                        self._run_action(page, action)

                    html = page.content()
                    browser.close()
                    return html
            except Exception as error:
                last_error = error
                logger.warning(
                    "Browser fetch failed (attempt %s/%s): %s",
                    attempt,
                    self.max_retries,
                    error,
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        raise FetchError(
            f"Failed to fetch {url} with browser after {self.max_retries} attempts: {last_error}"
        )

    @staticmethod
    def _run_action(page: Any, action: dict[str, Any]) -> None:
        """Run a single browser action on a Playwright page."""
        action_name = action["action"]
        selector = action.get("selector")

        if action_name == "wait_for_selector":
            page.wait_for_selector(selector, timeout=30000)
        elif action_name == "click":
            page.click(selector)
        elif action_name == "fill":
            page.fill(selector, action.get("value", ""))
        else:
            logger.warning("Unknown browser action: %s", action_name)