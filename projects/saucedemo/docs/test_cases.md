# Test Cases — SauceDemo

Detailed test cases for the scenarios marked "Yes" in [test_scenarios.md](test_scenarios.md).
Automation status reflects what is actually implemented under `tests/`. All cases assume
`base_url = https://www.saucedemo.com/` and, unless stated otherwise, password `secret_sauce`.

---

## Login (`tests/test_login.py`)

### TC-LOGIN-01 — Valid login with standard_user
- **Preconditions:** Browser open at the login page.
- **Test Data:** username `standard_user`, password `secret_sauce`.
- **Steps:** 1) Enter username. 2) Enter password. 3) Click Login.
- **Expected Result:** Redirected to `/inventory.html`; page title "Products" is visible; 6
  products are rendered.
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_valid_login`, marker `smoke`, `login`)

### TC-LOGIN-02 — Invalid username/password combination
- **Preconditions:** Browser open at the login page.
- **Test Data:** username `invalid_user`, password `wrong_password`.
- **Steps:** 1) Enter credentials. 2) Click Login.
- **Expected Result:** Error banner: "Epic sadface: Username and password do not match any user
  in this service". User remains on login page.
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_invalid_login`, parametrized, marker `regression`, `login`)

### TC-LOGIN-03 — Valid username with wrong password
- **Test Data:** username `standard_user`, password `not_the_real_password`.
- **Expected Result:** Same generic error banner as TC-LOGIN-02 (SauceDemo does not disclose which
  field is wrong — this is itself a behavior worth asserting on).
- **Priority:** P2 | **Severity:** Medium | **Automation:** Automated (part of the parametrized `test_invalid_login`)

### TC-LOGIN-04 — Empty username and password
- **Test Data:** username `""`, password `""`.
- **Expected Result:** Error banner: "Epic sadface: Username is required".
- **Priority:** P2 | **Severity:** Medium | **Automation:** Automated (part of the parametrized `test_invalid_login`)

### TC-LOGIN-05 — Locked-out user
- **Test Data:** username `locked_out_user`, password `secret_sauce`.
- **Expected Result:** Error banner: "Epic sadface: Sorry, this user has been locked out.".
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_locked_out_user_login`, marker `smoke`, `login`)

### TC-LOGOUT-01 — Logout from an authenticated session
- **Preconditions:** Logged in as `standard_user`.
- **Steps:** 1) Open burger menu. 2) Click Logout.
- **Expected Result:** Redirected to login page (`/`); login form is visible again.
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_logout`, marker `regression`, `login`)

---

## Products (`tests/test_products.py`)

### TC-PROD-01 — Inventory page lists all products
- **Preconditions:** Logged in as `standard_user`.
- **Expected Result:** Exactly 6 product cards are rendered, each with a non-empty name and a
  price formatted as `$X.XX`.
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_inventory_displays_all_products`, marker `smoke`)

### TC-PROD-02 — Sort products (A-Z / Z-A / low-high / high-low)
- **Preconditions:** Logged in as `standard_user`.
- **Test Data:** sort option in `{az, za, lohi, hilo}`.
- **Steps:** 1) Select sort option from dropdown.
- **Expected Result:** Displayed product order matches the expected order for that option
  (alphabetical or numeric, computed independently in the test — not hardcoded).
- **Priority:** P2 | **Severity:** Medium | **Automation:** Automated (`test_sort_products`, parametrized over all 4 options, marker `regression`)

### TC-PROD-03 — Open product detail page
- **Preconditions:** Logged in as `standard_user`.
- **Steps:** 1) Click a product's name/image on the inventory page.
- **Expected Result:** Detail page shows the same product name and price shown on the inventory
  card.
- **Priority:** P2 | **Severity:** Low | **Automation:** Automated (`test_open_product_details`, marker `regression`)

### TC-PROD-04 — Add product to cart from inventory page
- **Preconditions:** Logged in as `standard_user`, cart empty.
- **Steps:** 1) Click "Add to cart" for one product.
- **Expected Result:** Cart badge shows "1"; button label changes to "Remove".
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_add_product_to_cart_from_inventory`, marker `smoke`, `cart`)

### TC-PROD-05 — Add product to cart from product detail page
- **Preconditions:** Logged in as `standard_user`, on a product's detail page.
- **Steps:** 1) Click "Add to cart" on the detail page.
- **Expected Result:** Cart badge shows "1".
- **Priority:** P2 | **Severity:** Medium | **Automation:** Automated (`test_add_product_to_cart_from_product_page`, marker `regression`, `cart`)

---

## Cart (`tests/test_cart.py`)

### TC-CART-01 — Remove product from cart via inventory page
- **Preconditions:** Logged in, one product added to cart.
- **Steps:** 1) Click "Remove" on the inventory card.
- **Expected Result:** Cart badge disappears (no items); button reverts to "Add to cart".
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_remove_product_from_inventory_page`, marker `smoke`, `cart`)

### TC-CART-02 — Remove product from cart via cart page
- **Preconditions:** Logged in, one product added to cart, cart page open.
- **Steps:** 1) Click "Remove" next to the item in the cart.
- **Expected Result:** Item no longer listed; cart badge removed.
- **Priority:** P2 | **Severity:** Medium | **Automation:** Automated (`test_remove_product_from_cart_page`, marker `regression`, `cart`)

### TC-CART-03 — Cart reflects multiple added products
- **Preconditions:** Logged in as `standard_user`.
- **Test Data:** 3 distinct products.
- **Steps:** 1) Add 3 products from the inventory page. 2) Open cart.
- **Expected Result:** Cart lists exactly the 3 chosen product names, each with quantity 1 and the
  same price shown on the inventory page; badge shows "3".
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_cart_reflects_multiple_products`, marker `regression`, `cart`)

### TC-CART-04 — Cart persists across navigation back to products
- **Preconditions:** Logged in, product added to cart, cart page open.
- **Steps:** 1) Click "Continue Shopping". 2) Re-open cart.
- **Expected Result:** Previously added item is still present.
- **Priority:** P3 | **Severity:** Low | **Automation:** Automated (`test_cart_persists_after_continue_shopping`, marker `regression`, `cart`)

---

## Checkout (`tests/test_checkout.py`)

### TC-CHECKOUT-01 — Checkout information requires all fields
- **Preconditions:** Logged in, one product in cart, on checkout information step.
- **Test Data:** three variants — all fields empty, last name empty, postal code empty.
- **Steps:** 1) Fill only the non-empty fields per variant. 2) Click Continue.
- **Expected Result:** The corresponding "Error: <Field> is required" message is shown and the
  user stays on the information step.
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_checkout_requires_customer_information`, parametrized, marker `smoke`, `checkout`)

### TC-CHECKOUT-02 — Valid checkout information advances to overview
- **Preconditions:** Logged in, one product in cart.
- **Test Data:** First Name `John`, Last Name `Doe`, Postal Code `12345`.
- **Steps:** 1) Fill all three fields. 2) Click Continue.
- **Expected Result:** Redirected to the checkout overview (`/checkout-step-two.html`) showing the
  item, its price, and a payment/shipping summary.
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_valid_checkout_information_advances`, marker `smoke`, `checkout`)

### TC-CHECKOUT-03 — Overview totals are consistent
- **Preconditions:** On checkout overview with 2 known-price products in cart.
- **Expected Result:** `item total == sum(product prices)`; `total == item total + tax` (values
  parsed from the page, not hardcoded, so the assertion holds regardless of future price changes).
- **Priority:** P1 | **Severity:** High | **Automation:** Automated (`test_checkout_overview_totals_are_consistent`, marker `regression`, `checkout`)

### TC-CHECKOUT-04 — Complete an order
- **Preconditions:** On checkout overview with a valid cart.
- **Steps:** 1) Click Finish.
- **Expected Result:** Confirmation page shows header "Thank you for your order!" and the
  dispatch message; cart badge is cleared.
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_complete_order`, marker `smoke`, `checkout`)

---

## End-to-End (`tests/test_end_to_end.py`)

### TC-E2E-01 — Full purchase journey (showcase test)
- **Preconditions:** Fresh browser context, logged out.
- **Steps:** 1) Login as `standard_user`. 2) Sort products price low-to-high. 3) Add the cheapest
  and most expensive product to the cart. 4) Open cart and verify both items. 5) Checkout with
  valid customer information. 6) Verify overview totals. 7) Finish the order. 8) Verify
  confirmation message.
- **Expected Result:** Every step succeeds and the order confirmation is displayed at the end —
  proves the whole application flow works together, not just isolated units.
- **Priority:** P1 | **Severity:** Critical | **Automation:** Automated (`test_full_purchase_journey`, marker `smoke`, `e2e`)

---

## Documented but not automated

| ID | Reason |
|---|---|
| SC-06 (performance_glitch_user login) | Produces the same DOM/assertions as TC-LOGIN-01, only slower — automating it duplicates coverage without adding signal. Documented for manual/exploratory awareness. |
| SC-19 (checkout with empty cart) | SauceDemo does not block this path, and there's no unique business rule to verify beyond "overview shows 0 items" — low value relative to maintenance cost. |
| SC-26 (cancel checkout) | Straightforward navigation with no data-integrity risk; covered manually, not worth a dedicated automated case given the fixed time budget for this suite. |

See [automation_strategy.md](automation_strategy.md) for the full "why automate this" rationale.
