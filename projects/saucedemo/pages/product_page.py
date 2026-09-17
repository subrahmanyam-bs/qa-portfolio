"""Page object for a single product's detail page (/inventory-item.html?id=...)."""
from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.helpers import parse_price


class ProductPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.product_name = page.locator("[data-test='inventory-item-name']")
        self.product_price = page.locator("[data-test='inventory-item-price']")
        # Unlike the inventory/cart pages, the detail page's button carries a
        # generic data-test (no product slug) since only one item is ever shown.
        self.add_to_cart_button = page.locator("[data-test='add-to-cart']")
        self.remove_button = page.locator("[data-test='remove']")
        self.back_button = page.locator("[data-test='back-to-products']")

    def get_product_name(self) -> str:
        return self.product_name.inner_text()

    def get_product_price(self) -> float:
        return parse_price(self.product_price.inner_text())

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def back_to_products(self) -> None:
        self.back_button.click()
