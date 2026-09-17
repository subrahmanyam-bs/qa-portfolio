"""Checkout information, totals, and order completion. See docs/test_cases.md: TC-CHECKOUT-01..04."""
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.test_data import load_test_data

_CHECKOUT_INFO_CASES = load_test_data()["checkout_info"]["missing_field_cases"]


def _add_product_and_go_to_checkout(page, product_name: str) -> None:
    inventory_page = InventoryPage(page)
    inventory_page.add_product_to_cart(product_name)
    inventory_page.open_cart()
    CartPage(page).click_checkout()


@pytest.mark.smoke
@pytest.mark.checkout
@pytest.mark.parametrize(
    "case", _CHECKOUT_INFO_CASES, ids=[c["case_id"] for c in _CHECKOUT_INFO_CASES]
)
def test_checkout_requires_customer_information(logged_in_page, test_data, case):
    """TC-CHECKOUT-01: missing required fields block progress with a specific error."""
    _add_product_and_go_to_checkout(logged_in_page, test_data["products"]["backpack"])
    checkout_page = CheckoutPage(logged_in_page)

    checkout_page.enter_customer_information(
        case["first_name"], case["last_name"], case["postal_code"]
    )
    checkout_page.click_continue()

    assert checkout_page.get_error_message() == case["expected_error"]
    assert "checkout-step-one" in logged_in_page.url


@pytest.mark.smoke
@pytest.mark.checkout
def test_valid_checkout_information_advances(logged_in_page, test_data):
    """TC-CHECKOUT-02: valid customer information reaches the order overview."""
    _add_product_and_go_to_checkout(logged_in_page, test_data["products"]["backpack"])
    checkout_page = CheckoutPage(logged_in_page)
    info = test_data["checkout_info"]["valid"]

    checkout_page.enter_customer_information(
        info["first_name"], info["last_name"], info["postal_code"]
    )
    checkout_page.click_continue()

    logged_in_page.wait_for_url("**/checkout-step-two.html")


@pytest.mark.regression
@pytest.mark.checkout
def test_checkout_overview_totals_are_consistent(logged_in_page, test_data):
    """TC-CHECKOUT-03: item total + tax == total, using values read from the page."""
    inventory_page = InventoryPage(logged_in_page)
    prices_by_name = dict(
        zip(inventory_page.get_product_names(), inventory_page.get_product_prices())
    )
    chosen = [test_data["products"]["backpack"], test_data["products"]["onesie"]]
    for name in chosen:
        inventory_page.add_product_to_cart(name)
    inventory_page.open_cart()
    CartPage(logged_in_page).click_checkout()
    checkout_page = CheckoutPage(logged_in_page)
    info = test_data["checkout_info"]["valid"]
    checkout_page.enter_customer_information(
        info["first_name"], info["last_name"], info["postal_code"]
    )
    checkout_page.click_continue()
    logged_in_page.wait_for_url("**/checkout-step-two.html")

    expected_item_total = sum(prices_by_name[name] for name in chosen)
    assert checkout_page.get_item_total() == pytest.approx(expected_item_total)
    assert checkout_page.get_item_total() + checkout_page.get_tax() == pytest.approx(checkout_page.get_total())


@pytest.mark.smoke
@pytest.mark.checkout
def test_complete_order(logged_in_page, test_data):
    """TC-CHECKOUT-04: finishing the order shows the confirmation message and clears the cart."""
    _add_product_and_go_to_checkout(logged_in_page, test_data["products"]["backpack"])
    checkout_page = CheckoutPage(logged_in_page)
    info = test_data["checkout_info"]["valid"]
    checkout_page.enter_customer_information(
        info["first_name"], info["last_name"], info["postal_code"]
    )
    checkout_page.click_continue()
    logged_in_page.wait_for_url("**/checkout-step-two.html")

    checkout_page.finish_order()

    logged_in_page.wait_for_url("**/checkout-complete.html")
    assert checkout_page.get_confirmation_message() == "Thank you for your order!"
