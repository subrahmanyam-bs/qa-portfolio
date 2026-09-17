"""Login and logout behavior. See docs/test_cases.md: TC-LOGIN-01..05, TC-LOGOUT-01."""
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.test_data import load_test_data

_INVALID_LOGIN_CASES = load_test_data()["invalid_login_cases"]


@pytest.mark.smoke
@pytest.mark.login
def test_valid_login(page, base_url, test_data):
    """TC-LOGIN-01: standard_user reaches the inventory page and sees all products."""
    login_page = LoginPage(page)
    login_page.goto(base_url)
    user = test_data["users"]["standard"]

    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/inventory.html")

    inventory_page = InventoryPage(page)
    assert inventory_page.page_title.inner_text() == "Products"
    assert len(inventory_page.get_product_names()) == 6


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize(
    "case", _INVALID_LOGIN_CASES, ids=[c["case_id"] for c in _INVALID_LOGIN_CASES]
)
def test_invalid_login(page, base_url, case):
    """TC-LOGIN-02/03/04: wrong username, wrong password, and empty fields are all rejected."""
    login_page = LoginPage(page)
    login_page.goto(base_url)

    login_page.login(case["username"], case["password"])

    assert login_page.get_error_message() == case["expected_error"]
    assert page.url == base_url


@pytest.mark.smoke
@pytest.mark.login
def test_locked_out_user_login(page, base_url, test_data):
    """TC-LOGIN-05: locked_out_user is rejected with a specific lockout message."""
    login_page = LoginPage(page)
    login_page.goto(base_url)
    user = test_data["users"]["locked_out"]

    login_page.login(user["username"], user["password"])

    assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."


@pytest.mark.regression
@pytest.mark.login
def test_logout(logged_in_page, base_url):
    """TC-LOGOUT-01: logging out returns the user to the login page."""
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.logout()
    logged_in_page.wait_for_url(base_url)

    login_page = LoginPage(logged_in_page)
    assert login_page.login_button.is_visible()
