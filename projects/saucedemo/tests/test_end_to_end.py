"""Showcase test: the full purchase journey in one run. See docs/test_cases.md: TC-E2E-01."""
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.e2e
def test_full_purchase_journey(page, base_url, test_data):
    """Login -> browse/sort -> add products -> cart -> checkout -> confirmation.

    This exercises every page object together rather than in isolation, which is
    what actually proves the seams between pages still work (the focused tests in
    test_login/test_products/test_cart/test_checkout catch *where* something broke;
    this one catches *whether the whole flow still works end to end*).
    """
    user = test_data["users"]["standard"]
    login_page = LoginPage(page)
    login_page.goto(base_url)
    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/inventory.html")

    inventory_page = InventoryPage(page)
    inventory_page.sort_by("lohi")
    names = inventory_page.get_product_names()
    prices = inventory_page.get_product_prices()
    cheapest_name = names[0]
    most_expensive_name = names[-1]
    expected_item_total = prices[0] + prices[-1]

    inventory_page.add_product_to_cart(cheapest_name)
    inventory_page.add_product_to_cart(most_expensive_name)
    assert inventory_page.get_cart_badge_count() == 2

    inventory_page.open_cart()
    cart_page = CartPage(page)
    cart_item_names = {item["name"] for item in cart_page.get_cart_items()}
    assert cart_item_names == {cheapest_name, most_expensive_name}

    cart_page.click_checkout()
    checkout_page = CheckoutPage(page)
    info = test_data["checkout_info"]["valid"]
    checkout_page.enter_customer_information(
        info["first_name"], info["last_name"], info["postal_code"]
    )
    checkout_page.click_continue()
    page.wait_for_url("**/checkout-step-two.html")

    assert checkout_page.get_item_total() == pytest.approx(expected_item_total)
    assert checkout_page.get_item_total() + checkout_page.get_tax() == pytest.approx(checkout_page.get_total())

    checkout_page.finish_order()

    page.wait_for_url("**/checkout-complete.html")
    assert checkout_page.get_confirmation_message() == "Thank you for your order!"
