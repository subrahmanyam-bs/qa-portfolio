"""Shared pytest fixtures. Browser/context/page lifecycle is provided by the
pytest-playwright plugin (which also wires up the --browser/--headed/--slowmo CLI
flags); the fixtures below layer on top of it: app configuration, test data, a
pre-authenticated page, and automatic screenshot/trace capture on failure.
"""
from pathlib import Path

import pytest
from playwright.sync_api import Page

from utils.config_reader import load_config
from utils.test_data import load_test_data
from pages.login_page import LoginPage

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
TRACES_DIR = Path(__file__).parent / "traces"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stash each phase's result on the test item so fixtures can check pass/fail
    during teardown (request.node.rep_call is not otherwise available to fixtures).
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def config():
    """Application configuration merged from config/config.json and env var overrides."""
    return load_config()


@pytest.fixture(scope="session")
def base_url(config):
    """Overrides pytest-playwright's base_url fixture with our own config source."""
    return config["base_url"]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, config):
    """Lets config/config.json turn headless off by default for local debugging,
    without ever fighting an explicit --headed flag (which already produces the
    same result pytest-playwright's own fixture, so there's nothing to override
    when config asks for headless=True - that's the plugin's own default too).
    """
    if not config["headless"]:
        return {**browser_type_launch_args, "headless": False}
    return browser_type_launch_args


@pytest.fixture(scope="session")
def test_data():
    """Static test fixture data: users, products, checkout info. Loaded once per run."""
    return load_test_data()


@pytest.fixture(autouse=True)
def apply_default_timeout(page: Page, config):
    page.set_default_timeout(config["default_timeout_ms"])


@pytest.fixture(autouse=True)
def trace_on_failure(context, request):
    """Records a Playwright trace for every test, but only keeps the .zip when the
    test failed — passing tests don't need one, and this keeps traces/ from filling
    up with artifacts nobody will ever open.
    """
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        TRACES_DIR.mkdir(exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace("::", "_")
        context.tracing.stop(path=str(TRACES_DIR / f"{safe_name}.zip"))
    else:
        context.tracing.stop()


@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """Captures a screenshot only when a test fails, named after the failing test."""
    yield
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        SCREENSHOTS_DIR.mkdir(exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace("::", "_")
        page.screenshot(path=str(SCREENSHOTS_DIR / f"{safe_name}.png"))


@pytest.fixture
def logged_in_page(page: Page, base_url, test_data) -> Page:
    """Logs in as the standard user and hands back a page already on /inventory.html.

    Most cart/checkout/e2e tests don't care about login itself - this avoids
    repeating that boilerplate in every one of them.
    """
    login_page = LoginPage(page)
    login_page.goto(base_url)
    user = test_data["users"]["standard"]
    login_page.login(user["username"], user["password"])
    page.wait_for_url("**/inventory.html")
    return page
