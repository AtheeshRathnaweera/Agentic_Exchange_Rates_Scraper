from enum import Enum


class ScraperType(str, Enum):
    """
    Enumeration representing the supported scraper types for extracting exchange rates.

    Attributes:
        HTML: Scrapes data from HTML web pages.
        API: Retrieves data from API endpoints.
        PDF: Extracts data from PDF documents.
    """

    HTML = "html"
    API = "api"
    PDF = "pdf"
