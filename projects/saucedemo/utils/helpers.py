"""Small, stateless helpers shared across page objects and tests."""


def parse_price(price_text: str) -> float:
    """Convert a SauceDemo price string (e.g. "$29.99", "Item total: $37.98") to a float."""
    digits = price_text.split("$", 1)[1]
    return float(digits)
