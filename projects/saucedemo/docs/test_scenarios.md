# Test Scenarios — SauceDemo

Scope: `https://www.saucedemo.com/`. Scenarios are grouped by feature area and mapped to the
detailed test cases in [test_cases.md](test_cases.md). Automation decisions are explained in
[automation_strategy.md](automation_strategy.md).

Legend — **Priority**: P1 (critical path) / P2 (important) / P3 (nice-to-have).
**Type**: Functional / UI / Negative / Edge.

| Scenario ID | Description | Priority | Test Type | Expected Result | Automation Candidate |
|---|---|---|---|---|---|
| SC-01 | Login with valid standard user credentials | P1 | Functional | User is redirected to the inventory page and products are visible | Yes |
| SC-02 | Login with invalid username/password combination | P1 | Negative | Login is rejected with an error banner, user stays on login page | Yes |
| SC-03 | Login with valid username but wrong password | P2 | Negative | Login is rejected with the same generic error banner | Yes |
| SC-04 | Login with empty username and/or password | P2 | Negative | Field-specific required error is shown | Yes |
| SC-05 | Login with locked-out user | P1 | Negative | Error banner states the user has been locked out | Yes |
| SC-06 | Login with performance_glitch_user | P3 | Functional | User eventually reaches inventory page (slower response) | No |
| SC-07 | Logout from an authenticated session | P1 | Functional | User is returned to the login page and session state is cleared | Yes |
| SC-08 | Verify all 6 inventory products render with name, price, and image | P1 | Functional | 6 products are listed, each with non-empty name and price | Yes |
| SC-09 | Sort products by Name (A to Z) | P2 | Functional | Product list order matches alphabetical ascending order | Yes |
| SC-10 | Sort products by Name (Z to A) | P2 | Functional | Product list order matches alphabetical descending order | Yes |
| SC-11 | Sort products by Price (low to high) | P2 | Functional | Product list order matches ascending price order | Yes |
| SC-12 | Sort products by Price (high to low) | P2 | Functional | Product list order matches descending price order | Yes |
| SC-13 | Open a product's detail page from the inventory list | P2 | Functional | Detail page shows the same name and price as the inventory card | Yes |
| SC-14 | Add a single product to the cart from the inventory page | P1 | Functional | Cart badge shows 1 and button label changes to Remove | Yes |
| SC-15 | Add a product to the cart from the product detail page | P2 | Functional | Cart badge increments and item appears in cart | Yes |
| SC-16 | Remove a product from the cart via the inventory page | P1 | Functional | Cart badge decrements/disappears and button reverts to Add to cart | Yes |
| SC-17 | Remove a product from the cart via the cart page | P2 | Functional | Item no longer listed in the cart | Yes |
| SC-18 | Add multiple products and verify cart contents | P1 | Functional | Cart lists correct names, prices, and quantity for each item | Yes |
| SC-19 | Proceed to checkout with an empty cart | P3 | Edge | Checkout page/overview shows zero items, no error | No |
| SC-20 | Submit checkout information form with all fields empty | P1 | Negative | Error: First Name is required | Yes |
| SC-21 | Submit checkout information form missing last name | P2 | Negative | Error: Last Name is required | Yes |
| SC-22 | Submit checkout information form missing postal code | P2 | Negative | Error: Postal Code is required | Yes |
| SC-23 | Submit valid checkout information | P1 | Functional | User advances to the checkout overview page | Yes |
| SC-24 | Verify checkout overview totals (item total, tax, total) | P1 | Functional | Displayed total equals item total plus tax | Yes |
| SC-25 | Complete an order from the checkout overview | P1 | Functional | Confirmation page shows "Thank you for your order" | Yes |
| SC-26 | Cancel checkout from the information step | P3 | Functional | User returns to the inventory page, cart is preserved | No |
| SC-27 | Full end-to-end purchase journey (login → browse → cart → checkout → confirmation) | P1 | Functional | Order completes successfully and confirmation is displayed | Yes |
