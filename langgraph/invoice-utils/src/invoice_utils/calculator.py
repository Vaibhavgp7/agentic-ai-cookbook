"""Line-item and discount calculations."""


def line_total(quantity: int, unit_price: float) -> float:
    """Return total for a single line item."""
    if quantity < 0:
        raise ValueError("quantity must be non-negative")
    if unit_price < 0:
        raise ValueError("unit_price must be non-negative")
    return round(quantity * unit_price, 2)


def apply_discount(subtotal: float, discount_percent: float) -> float:
    """Apply a percentage discount and return the discounted total."""
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    return round(subtotal * (1 - discount_percent / 100), 2)
