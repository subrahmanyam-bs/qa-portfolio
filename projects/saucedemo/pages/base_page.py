"""Shared base class for all SauceDemo page objects."""
from playwright.sync_api import Page


class BasePage:
    """Holds the Playwright page and any navigation helper common to every page object."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)
