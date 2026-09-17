"""Cart add/remove and validation behavior. See docs/test_cases.md: TC-CART-01..04."""
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.cart
def test_remove_product_from_inventory_page(logged_in_page, test_data):
    """TC-CART-01: removing via the inventory page clears the cart badge."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["backpack"]
    inventory_page.add_product_to_cart(product_name)
    assert inventory_page.get_cart_badge_count() == 1

    inventory_page.remove_product_from_cart(product_name)

    assert inventory_page.get_cart_badge_count() == 0


@pytest.mark.regression
@pytest.mark.cart
def test_remove_product_from_cart_page(logged_in_page, test_data):
    """TC-CART-02: removing via the cart page drops the item from the cart list."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["backpack"]
    inventory_page.add_product_to_cart(product_name)
    inventory_page.open_cart()
    cart_page = CartPage(logged_in_page)

    cart_page.remove_product(product_name)

    assert cart_page.get_cart_items() == []


@pytest.mark.regression
@pytest.mark.cart
def test_cart_reflects_multiple_products(logged_in_page, test_data):
    """TC-CART-03: the cart lists correct name/price/quantity for every added product."""
    inventory_page = InventoryPage(logged_in_page)
    product_names = [
        test_data["products"]["backpack"],
        test_data["products"]["bike_light"],
        test_data["products"]["onesie"],
    ]
    expected_prices = dict(
        zip(inventory_page.get_product_names(), inventory_page.get_product_prices())
    )
    for name in product_names:
        inventory_page.add_product_to_cart(name)
    assert inventory_page.get_cart_badge_count() == 3

    inventory_page.open_cart()
    cart_page = CartPage(logged_in_page)
    cart_items = cart_page.get_cart_items()

    assert {item["name"] for item in cart_items} == set(product_names)
    for item in cart_items:
        assert item["quantity"] == 1
        assert item["price"] == expected_prices[item["name"]]


@pytest.mark.regression
@pytest.mark.cart
def test_cart_persists_after_continue_shopping(logged_in_page, test_data):
    """TC-CART-04: navigating back to products and re-opening the cart keeps the item."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["fleece_jacket"]
    inventory_page.add_product_to_cart(product_name)
    inventory_page.open_cart()
    cart_page = CartPage(logged_in_page)

    cart_page.continue_shopping()
    inventory_page.open_cart()

    cart_items = cart_page.get_cart_items()
    assert [item["name"] for item in cart_items] == [product_name]
