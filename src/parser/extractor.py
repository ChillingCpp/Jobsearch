"""HTML parser that extracts raw job data using website configuration."""

from dataclasses import dataclass

from bs4 import BeautifulSoup

from src.core.config import WebsiteConfig


@dataclass
class RawJob:
    """Raw job data extracted from HTML, before normalization."""

    title: str = ""
    company: str = ""
    description: str = ""
    url: str = ""
    salary: str = ""
    location: str = ""
    posted_date: str = ""


class Parser:
    """Extracts raw job data from HTML using a website configuration."""

    def parse(self, html: str, config: WebsiteConfig) -> list[RawJob]:
        """Parse HTML and return a list of raw jobs.

        Args:
            html: The page HTML to parse.
            config: The website configuration with selectors.

        Returns:
            A list of RawJob objects. Empty if no job listings are found.
        """
        soup = BeautifulSoup(html, "html.parser")
        listing_selector = config.selectors.get("job_listing")

        if not listing_selector:
            return []

        listings = soup.select(listing_selector)
        jobs: list[RawJob] = []

        for listing in listings:
            jobs.append(self._extract_job(listing, config))

        return jobs

    @staticmethod
    def _extract_job(listing, config: WebsiteConfig) -> RawJob:
        """Extract a single RawJob from a job listing element."""
        selectors = config.selectors

        def text_of(key: str) -> str:
            selector = selectors.get(key)
            if not selector:
                return ""
            element = listing.select_one(selector)
            if element is None:
                return ""
            return element.get_text(strip=True)

        def href_of(key: str) -> str:
            selector = selectors.get(key)
            if not selector:
                return ""
            element = listing.select_one(selector)
            if element is None:
                return ""
            return element.get("href", "")

        return RawJob(
            title=text_of("title"),
            company=text_of("company"),
            description=text_of("description"),
            url=href_of("url"),
            salary=text_of("salary"),
            location=text_of("location"),
            posted_date=text_of("posted_date"),
        )