"""Page object covering the full checkout flow: customer info, overview, and completion."""
from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.helpers import parse_price


class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Step one - customer information
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.error_message = page.locator("[data-test='error']")

        # Step two - order overview
        self.item_total_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")

        # Step three - confirmation
        self.complete_header = page.locator("[data-test='complete-header']")
        self.complete_text = page.locator("[data-test='complete-text']")

    # --- Step one -----------------------------------------------------
    def enter_customer_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def click_continue(self) -> None:
        self.continue_button.click()

    def get_error_message(self) -> str:
        self.error_message.wait_for(state="visible")
        return self.error_message.inner_text()

    # --- Step two -------------------------------------------------------
    def get_item_total(self) -> float:
        return parse_price(self.item_total_label.inner_text())

    def get_tax(self) -> float:
        return parse_price(self.tax_label.inner_text())

    def get_total(self) -> float:
        return parse_price(self.total_label.inner_text())

    def finish_order(self) -> None:
        self.finish_button.click()

    # --- Step three -----------------------------------------------------
    def get_confirmation_message(self) -> str:
        self.complete_header.wait_for(state="visible")
        return self.complete_header.inner_text()
