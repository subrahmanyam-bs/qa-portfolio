# SauceDemo UI Automation Framework

A Page Object Model UI automation suite for [SauceDemo](https://www.saucedemo.com/), built with
Python, Playwright, and Pytest. This is a QA automation portfolio project — it's scoped and
documented the way I'd set up and hand off a real regression suite, not a demo script.

## 1. Project Overview

SauceDemo is a purpose-built e-commerce demo app (login → browse/sort products → cart → checkout
→ order confirmation). This repository automates its critical user journeys with a maintainable
Page Object Model framework: 25 tests across login, product listing/sorting, cart, checkout, and
one end-to-end purchase flow, backed by design documents that explain *why* each test exists.

## 2. Application Under Test

- **URL:** https://www.saucedemo.com/
- **Type:** Client-rendered single-page app (React), fixed catalog of 6 products, no backend
  persistence — every test run starts from the same known state.
- **Test accounts:** `standard_user`, `locked_out_user`, and others, all with password
  `secret_sauce`, documented in the app's own login page and in `test_data/test_data.json`.

## 3. Objective

Demonstrate the skills a QA automation engineer actually uses day-to-day: scenario/test-case
design before automation, a POM framework that survives UI churn, sensible fixture and config
management, meaningful assertions, CI integration, and a repo a recruiter can skim and understand
in five minutes.

## 4. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.12 | Widely used for automation, readable, strong ecosystem |
| Browser automation | Playwright (sync API) | Auto-waiting, reliable selectors, built-in tracing |
| Test runner | Pytest | Fixtures, markers, parametrization, huge plugin ecosystem |
| Plugins | pytest-playwright, pytest-html, pytest-xdist | Browser lifecycle + CLI flags, HTML reporting, parallel execution |
| CI | GitHub Actions | Free, standard, plugs directly into `pytest` |

## 5. Framework Architecture

Page Object Model with a thin `BasePage`, one page object per screen, tests that read as business
behavior (not raw Playwright calls), fixtures for setup/teardown, and JSON-based configuration and
test data kept out of the code.

```
Test (business behavior)
   -> Page Object (actions/queries on one screen)
      -> Playwright Page (browser automation)
```

Assertions live in the tests, not the page objects — a page object answers "what can you do on
this screen and what can you read from it," a test answers "is that correct."

## 6. Folder Structure

```
saucedemo/
├── docs/                       Test design artifacts (written before automation)
│   ├── test_scenarios.md
│   ├── test_cases.md
│   └── automation_strategy.md
├── pages/                      Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                      Pytest test suites (business-readable)
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_end_to_end.py
├── utils/
│   ├── config_reader.py        Loads config/config.json + env overrides
│   ├── test_data.py             Loads test_data/test_data.json
│   └── helpers.py               Small shared helpers (price parsing)
├── test_data/test_data.json     Users, products, checkout data
├── config/config.json           base_url, browser, headless, timeout
├── reports/                     Generated pytest-html reports (gitignored contents)
├── screenshots/                 Failure screenshots only (gitignored contents)
├── traces/                      Failure traces only (gitignored contents)
├── .github/workflows/tests.yml  CI pipeline
├── conftest.py                  Fixtures + failure-artifact hooks
├── pytest.ini                   Markers, default report options
├── requirements.txt
├── .env.example
└── .gitignore
```

## 7. Test Coverage

25 automated tests across 5 suites — see [docs/test_scenarios.md](docs/test_scenarios.md) for the
full scenario list and [docs/test_cases.md](docs/test_cases.md) for step-by-step test cases.

| Area | Tests | Highlights |
|---|---|---|
| Login/Logout | 6 | valid login, 3 invalid-credential variants, locked-out user, logout |
| Products | 8 | listing, all 4 sort orders, detail page, add-to-cart (2 entry points) |
| Cart | 4 | remove from 2 entry points, multi-product validation, persistence |
| Checkout | 6 | 3 missing-field variants, valid submission, totals consistency, completion |
| End-to-end | 1 | full login → browse → cart → checkout → confirmation showcase flow |

## 8. Test Scenarios

`docs/test_scenarios.md` lists 27 scenarios (Scenario ID, description, priority, type, expected
result, automation candidate) covering the full feature surface — including scenarios that were
deliberately **not** automated, with the reasoning documented rather than silently dropped.

## 9. POM Explanation

Each page object exposes:
- **Locators** as `__init__` attributes (so they're visible at a glance, not buried in methods).
- **Action methods** (`click_login`, `add_product_to_cart`) that do one thing.
- **Query methods** (`get_error_message`, `get_cart_items`) that return data for the test to
  assert on — page objects never assert.
- **Composite methods** (`login()`, `finish_order()`) for the common multi-step actions tests
  actually need, so tests don't re-implement the same 3-step sequence everywhere.

Example — `InventoryPage.add_product_to_cart` scopes to the specific product card instead of
guessing SauceDemo's generated button ID:

```python
def add_product_to_cart(self, product_name: str) -> None:
    self._item_card(product_name).get_by_role("button", name="Add to cart").click()
```

## 10. Fixture Strategy

Defined in `conftest.py`, layered on top of `pytest-playwright`'s own `browser`/`context`/`page`
fixtures (reused, not reinvented — this is also what gives us `--browser`/`--headed` for free):

| Fixture | Scope | Purpose |
|---|---|---|
| `config` | session | App config from `config/config.json` + env overrides |
| `base_url` | session | Overrides pytest-playwright's `base_url` with our config source |
| `test_data` | session | Users/products/checkout data loaded once per run |
| `apply_default_timeout` | function, autouse | Applies `config`'s timeout to every page |
| `trace_on_failure` | function, autouse | Starts tracing per test, keeps the `.zip` only on failure |
| `screenshot_on_failure` | function, autouse | Captures a screenshot only on failure |
| `logged_in_page` | function | Logs in as `standard_user`, returns a page on `/inventory.html` |

`context`/`page` must stay function-scoped for test isolation (and to be safe under `-n` parallel
execution — sharing a browser context across tests would leak cookies/cart state between them).
`config`/`test_data` are read-only and static, so session scope avoids re-reading the same JSON
file 25 times for no benefit.

## 11. Locator Strategy

SauceDemo ships explicit `data-test` attributes on nearly every interactive element — those are
used as the primary locator strategy since they're purpose-built test hooks and don't shift when
CSS classes or copy change. `get_by_role`/`get_by_text` are used where no `data-test` exists (e.g.
the product-card "Add to cart"/"Remove" buttons are matched by accessible role + name, scoped to
the product's card, rather than by SauceDemo's generated per-product ID — that avoids a brittle
slug like `add-to-cart-test.allthethings()-t-shirt-(red)` entirely). One CSS `id` selector
(`#react-burger-menu-btn`) is used for the hamburger menu button, which has no `data-test` of its
own on the element that actually owns the click handler. No hard-coded XPath, no `time.sleep()` —
all waits go through Playwright's auto-waiting or explicit `wait_for`/`wait_for_url`.

## 12. Test Data Strategy

`test_data/test_data.json` holds users, product names, checkout info, and parametrized negative
cases, separate from test logic. Tests load it through `utils/test_data.py` (a fixture for runtime
use, plus a direct import at module load time for building `@pytest.mark.parametrize` lists, since
fixtures aren't available at collection time). No secrets are stored — SauceDemo's test accounts
are public fixture data documented on the login page itself.

## 13. Reporting

Every run generates a self-contained HTML report via `pytest-html`:

```bash
pytest                      # writes reports/report.html automatically (see pytest.ini addopts)
```

Open `reports/report.html` in a browser for pass/fail counts, duration per test, and full
tracebacks for failures.

## 14. Screenshot Handling

`screenshot_on_failure` (autouse, in `conftest.py`) captures one screenshot per failing test into
`screenshots/`, named after the test (e.g. `test_valid_login[chromium].png`). No screenshots are
taken on passing tests — the folder only ever contains signal, not noise.

## 15. Trace Viewer

`trace_on_failure` starts a Playwright trace at the beginning of every test and saves it to
`traces/` only when the test fails. To inspect one:

```bash
playwright show-trace traces/test_valid_login[chromium].zip
```

This opens Playwright's trace viewer — a timeline of every action, network request, and DOM
snapshot for that test run, which is dramatically faster for debugging a CI failure than re-running
locally and hoping to reproduce it.

## 16. Cross-Browser Testing

Browser selection is a CLI flag, not a code change (via `pytest-playwright`):

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

All three engines were exercised during development of this suite (Firefox run included below).

## 17. Parallel Execution

```bash
pytest -n 2
pytest -n auto
```

Safe by construction: `context`/`page` fixtures are function-scoped, so each test gets its own
isolated browser context (own cookies, own cart state) regardless of how many workers run
concurrently.

## 18. Installation

```bash
git clone <this-repo>
cd saucedemo
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install
```

## 19. Setup

Copy `.env.example` to `.env` if you want to override the base URL (e.g. against a staging
environment); no other configuration is required to run against the public SauceDemo site.

```bash
cp .env.example .env
```

`config/config.json` holds `base_url`, `default_timeout_ms` (both applied via fixtures every run),
and `browser`/`headless` as documented defaults — browser selection is normally driven by the
`--browser` CLI flag, and `headless: false` in the config can flip the default to headed locally
without needing `--headed` on every command, without ever fighting an explicit `--headed` flag.

## 20. How to Run Tests

```bash
pytest                              # full suite, headless chromium
pytest -v                           # verbose output
pytest tests/test_login.py          # a single suite
pytest tests/test_login.py::test_valid_login   # a single test
pytest --headed                     # watch it run in a real browser window
pytest --browser firefox            # run against Firefox instead
```

## 21. How to Run Smoke Tests

```bash
pytest -m smoke
```

11 tests covering the critical path (login, add-to-cart, checkout completion, the E2E showcase) —
what should gate a merge.

## 22. How to Run Regression Tests

```bash
pytest -m regression
```

14 tests covering the broader surface (sort orders, secondary entry points, edge-case validation)
— for a scheduled/nightly run or before a release.

## 23. How to Generate Reports

```bash
pytest                          # reports/report.html is generated automatically
```

`pytest.ini` wires `--html=reports/report.html --self-contained-html` into the default options, so
no extra flags are needed for local runs.

## 24. How to Debug Failed Tests

1. Check `reports/report.html` for the failing assertion and traceback.
2. Check `screenshots/<test-name>.png` for what the page looked like at the moment of failure.
3. Open `traces/<test-name>.zip` with `playwright show-trace` for a full action-by-action replay.
4. Reproduce locally with `pytest tests/test_x.py::test_y --headed --browser chromium` to watch it
   live.

## 25. Sample Test Execution

```
$ pytest -v
tests/test_cart.py::test_remove_product_from_inventory_page[chromium] PASSED       [  4%]
tests/test_cart.py::test_remove_product_from_cart_page[chromium] PASSED            [  8%]
tests/test_checkout.py::test_checkout_requires_customer_information[chromium-all_fields_empty] PASSED [ 20%]
tests/test_checkout.py::test_valid_checkout_information_advances[chromium] PASSED  [ 32%]
tests/test_end_to_end.py::test_full_purchase_journey[chromium] PASSED              [ 44%]
tests/test_login.py::test_valid_login[chromium] PASSED                             [ 48%]
tests/test_products.py::test_sort_products[chromium-lohi] PASSED                   [ 84%]
...
25 passed in 35.98s
```

Cross-browser run (Firefox, login suite):

```
$ pytest tests/test_login.py -v --browser firefox
tests/test_login.py::test_valid_login[firefox] PASSED
tests/test_login.py::test_invalid_login[firefox-wrong_username_and_password] PASSED
tests/test_login.py::test_invalid_login[firefox-valid_username_wrong_password] PASSED
tests/test_login.py::test_invalid_login[firefox-empty_credentials] PASSED
tests/test_login.py::test_locked_out_user_login[firefox] PASSED
tests/test_login.py::test_logout[firefox] PASSED
6 passed in 14.86s
```

Parallel run:

```
$ pytest -n 2
25 passed in 22.14s
```

## 26. Future Enhancements

- Visual regression testing (Playwright screenshot comparison) for pixel-level UI checks — out of
  scope here since this suite targets functional behavior, not visual polish.
- API-level seeding/teardown if SauceDemo ever exposes a backend, to decouple UI tests from UI-only
  state setup.
- Allure reporting if the team already has Allure infrastructure — skipped here to avoid an
  unnecessary Java dependency for a project meant to run with `pip install` alone.
- A `docker-compose` runner for fully reproducible CI-identical local runs.

## 27. Skills Demonstrated

Manual test design (scenarios/test cases before automation) · Python · Playwright · Pytest ·
Page Object Model · fixture design and scoping · stable locator strategy · meaningful assertions
(including floating-point-safe comparisons with `pytest.approx`) · parametrized testing ·
JSON-based configuration and test data management · HTML reporting · failure-only screenshot and
trace capture · cross-browser and parallel execution · CI/CD with GitHub Actions · Git/GitHub
project hygiene (`.gitignore`, `.env.example`, no secrets committed).

---

## Why These Tests Were Automated

Automating everything possible isn't the goal — a suite that catches real regressions cheaply and
stays cheap to maintain is. Full reasoning, including what was **deliberately left out** (and why),
is in [docs/automation_strategy.md](docs/automation_strategy.md). Short version: every automated
test sits on a critical path, has a deterministic outcome, and asserts against values read from the
page rather than hardcoded snapshots — so the suite doesn't rot when SauceDemo's fixture data
shifts.
