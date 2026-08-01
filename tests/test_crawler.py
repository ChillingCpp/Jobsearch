"""Tests for the crawler fetcher."""

import pytest
import requests
from unittest.mock import Mock, patch

from src.crawler.fetcher import FetchError, Fetcher


def make_response(status_code: int = 200, text: str = "<html>ok</html>") -> Mock:
    """Create a mock requests response."""
    response = Mock()
    response.status_code = status_code
    response.text = text
    response.raise_for_status = Mock(
        side_effect=requests.HTTPError() if status_code >= 400 else None
    )
    return response


def test_fetch_returns_html() -> None:
    """A successful fetch returns the page HTML."""
    fetcher = Fetcher(max_retries=3, retry_delay=0)
    expected_html = "<html><body>Jobs</body></html>"

    with patch("src.crawler.fetcher.requests.get", return_value=make_response(text=expected_html)) as mock_get:
        html = fetcher.fetch("https://example.com/jobs")

    assert html == expected_html
    mock_get.assert_called_once_with("https://example.com/jobs", headers=None, timeout=30)


def test_fetch_retries_on_failure_then_succeeds() -> None:
    """Fetch retries on failure and succeeds on a later attempt."""
    fetcher = Fetcher(max_retries=3, retry_delay=0)

    responses = [
        make_response(status_code=500),
        make_response(status_code=500),
        make_response(text="<html>retried</html>"),
    ]

    with patch("src.crawler.fetcher.requests.get", side_effect=responses) as mock_get:
        html = fetcher.fetch("https://example.com/jobs")

    assert html == "<html>retried</html>"
    assert mock_get.call_count == 3


def test_fetch_raises_after_exhausting_retries() -> None:
    """Fetch raises FetchError after all retries fail."""
    fetcher = Fetcher(max_retries=2, retry_delay=0)

    with patch("src.crawler.fetcher.requests.get", side_effect=requests.ConnectionError("down")):
        with pytest.raises(FetchError):
            fetcher.fetch("https://example.com/jobs")


def test_fetch_accepts_custom_headers() -> None:
    """Custom headers are passed to the request."""
    fetcher = Fetcher(max_retries=1, retry_delay=0)
    headers = {"User-Agent": "TestAgent"}

    with patch("src.crawler.fetcher.requests.get", return_value=make_response(text="<html>h</html>")) as mock_get:
        fetcher.fetch("https://example.com/jobs", headers=headers)

    mock_get.assert_called_once_with("https://example.com/jobs", headers=headers, timeout=30)