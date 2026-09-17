"""Product listing, sorting, and detail-page behavior. See docs/test_cases.md: TC-PROD-01..05."""
import pytest

from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage


@pytest.mark.smoke
def test_inventory_displays_all_products(logged_in_page):
    """TC-PROD-01: all 6 fixed inventory items render with a name and a price."""
    inventory_page = InventoryPage(logged_in_page)

    names = inventory_page.get_product_names()
    prices = inventory_page.get_product_prices()

    assert len(names) == 6
    assert all(name.strip() for name in names)
    assert all(price > 0 for price in prices)


@pytest.mark.regression
@pytest.mark.parametrize("sort_option", ["az", "za", "lohi", "hilo"])
def test_sort_products(logged_in_page, sort_option):
    """TC-PROD-02: each sort option reorders the list to match an independently
    computed expected order, rather than a hardcoded snapshot of today's data.
    """
    inventory_page = InventoryPage(logged_in_page)
    baseline = list(zip(inventory_page.get_product_names(), inventory_page.get_product_prices()))

    inventory_page.sort_by(sort_option)
    actual_names = inventory_page.get_product_names()

    if sort_option == "az":
        expected = sorted(baseline, key=lambda item: item[0])
    elif sort_option == "za":
        expected = sorted(baseline, key=lambda item: item[0], reverse=True)
    elif sort_option == "lohi":
        expected = sorted(baseline, key=lambda item: item[1])
    else:  # hilo
        expected = sorted(baseline, key=lambda item: item[1], reverse=True)

    assert actual_names == [name for name, _ in expected]


@pytest.mark.regression
def test_open_product_details(logged_in_page, test_data):
    """TC-PROD-03: the detail page shows the same name and price as the inventory card."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["backpack"]
    expected_price = dict(
        zip(inventory_page.get_product_names(), inventory_page.get_product_prices())
    )[product_name]

    inventory_page.open_product(product_name)

    product_page = ProductPage(logged_in_page)
    assert product_page.get_product_name() == product_name
    assert product_page.get_product_price() == expected_price


@pytest.mark.smoke
@pytest.mark.cart
def test_add_product_to_cart_from_inventory(logged_in_page, test_data):
    """TC-PROD-04: adding a product updates the cart badge to 1."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["backpack"]

    inventory_page.add_product_to_cart(product_name)

    assert inventory_page.get_cart_badge_count() == 1


@pytest.mark.regression
@pytest.mark.cart
def test_add_product_to_cart_from_product_page(logged_in_page, test_data):
    """TC-PROD-05: adding to cart from the detail page also updates the badge."""
    inventory_page = InventoryPage(logged_in_page)
    product_name = test_data["products"]["bike_light"]
    inventory_page.open_product(product_name)
    product_page = ProductPage(logged_in_page)

    product_page.add_to_cart()

    product_page.back_to_products()
    assert inventory_page.get_cart_badge_count() == 1
