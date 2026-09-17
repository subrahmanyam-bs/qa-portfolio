"""Page object for the SauceDemo product listing page (/inventory.html)."""
from typing import List

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from utils.helpers import parse_price


class InventoryPage(BasePage):
    URL_PATH = "inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_title = page.locator("[data-test='title']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.product_names = page.locator("[data-test='inventory-item-name']")
        self.product_prices = page.locator("[data-test='inventory-item-price']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        # The hamburger menu icon has no data-test hook of its own and overlays the
        # button that owns the click handler, so it's addressed by its stable id.
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")

    def _item_card(self, product_name: str) -> Locator:
        return self.page.locator("[data-test='inventory-item']").filter(has_text=product_name)

    def get_product_names(self) -> List[str]:
        return self.product_names.all_inner_texts()

    def get_product_prices(self) -> List[float]:
        return [parse_price(text) for text in self.product_prices.all_inner_texts()]

    def sort_by(self, option_value: str) -> None:
        """option_value is one of: az, za, lohi, hilo."""
        self.sort_dropdown.select_option(option_value)

    def add_product_to_cart(self, product_name: str) -> None:
        self._item_card(product_name).get_by_role("button", name="Add to cart").click()

    def remove_product_from_cart(self, product_name: str) -> None:
        self._item_card(product_name).get_by_role("button", name="Remove").click()

    def open_product(self, product_name: str) -> None:
        self._item_card(product_name).get_by_role(
            "button", name=f"View details for {product_name}"
        ).first.click()

    def open_cart(self) -> None:
        self.cart_link.click()

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
