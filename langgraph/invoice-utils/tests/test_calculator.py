import pytest

from invoice_utils.calculator import line_total, apply_discount


def test_line_total_basic():
    assert line_total(3, 10.0) == 30.0


def test_line_total_rounds():
    assert line_total(2, 4.995) == 9.99


def test_line_total_rejects_negative_quantity():
    with pytest.raises(ValueError, match="quantity"):
        line_total(-1, 10.0)


def test_apply_discount():
    assert apply_discount(100.0, 10) == 90.0


def test_apply_discount_invalid_percent():
    with pytest.raises(ValueError, match="discount_percent"):
        apply_discount(100.0, 150)
