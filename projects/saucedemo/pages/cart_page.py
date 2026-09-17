"""Page object for the SauceDemo cart page (/cart.html)."""
from typing import Dict, List

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage
from utils.helpers import parse_price


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_items = page.locator("[data-test='inventory-item']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def _item_row(self, product_name: str) -> Locator:
        return self.cart_items.filter(has_text=product_name)

    def get_cart_items(self) -> List[Dict[str, object]]:
        """Return [{"name": str, "price": float, "quantity": int}, ...] for every cart row."""
        items = []
        for row in self.cart_items.all():
            items.append(
                {
                    "name": row.locator("[data-test='inventory-item-name']").inner_text(),
                    "price": parse_price(row.locator("[data-test='inventory-item-price']").inner_text()),
                    "quantity": int(row.locator("[data-test='item-quantity']").inner_text()),
                }
            )
        return items

    def remove_product(self, product_name: str) -> None:
        self._item_row(product_name).get_by_role("button", name="Remove").click()

    def click_checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
