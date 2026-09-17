# Automation Strategy — Why These Tests Were Automated

This document explains the reasoning behind what got automated in this suite, not just what did.
Automating everything that *could* be automated isn't the goal — the goal is a suite that catches
real regressions cheaply and stays cheap to maintain.

## Selection criteria

A scenario was automated when it met at least two of the following:

1. **It sits on the critical user path** (login, add to cart, checkout, order completion) — a
   regression here breaks the core business flow, so the cost of a false negative is high.
2. **It has a deterministic, verifiable outcome** — a specific error string, a specific product
   order, a specific total — not something that requires human judgement (visual polish, copy
   tone, etc).
3. **It is cheap to keep green** — the assertion is based on data read from the page (prices,
   totals) rather than values hardcoded from today's snapshot, so the test doesn't rot when
   SauceDemo's fixture data shifts.
4. **It would be tedious/error-prone to check manually every release** — e.g. verifying 4 sort
   orders, or that cart totals reconcile after adding several items.

## What was deliberately left out, and why

- **`performance_glitch_user` login** — behaves identically to `standard_user` except for an
  artificial delay. There is no additional assertion this user unlocks; automating it would just
  be `test_valid_login` again with a slower `page.wait_for_*`. Documented instead in
  [test_cases.md](test_cases.md) as a manual/exploratory note.
- **Checkout with an empty cart** — SauceDemo doesn't guard against it, and there's no business
  rule to protect (no "cart empty" error state exists). Testing it mainly verifies "the app
  doesn't crash," which is better exploratory-tested once than maintained as a permanent CI check.
- **Cancel-from-checkout navigation** — pure navigation with no state-integrity risk (nothing is
  charged, nothing is persisted server-side to be corrupted). Low risk, low payoff for automation.
- **Visual/pixel-level checks** (image rendering, CSS layout) — out of scope for a functional UI
  suite; would require a visual-regression tool, which is a separate investment decision, not a
  gap in this suite's design.

## Coverage shape

The suite intentionally weights toward the checkout funnel (login → cart → checkout → confirm)
because that is where SauceDemo's actual business logic lives (validation rules, price/tax
arithmetic, state transitions). Product listing/sorting is covered but kept lighter, since it's
mostly static content rendering.

One end-to-end test (`test_full_purchase_journey`) exists on top of the focused unit-style tests
deliberately: the focused tests catch *where* something broke quickly; the E2E test catches
*whether the seams between pages still work together*, which the focused tests can't prove on
their own.
