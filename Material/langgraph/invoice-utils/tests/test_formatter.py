from invoice_utils.formatter import format_currency


def test_format_usd():
    assert format_currency(1234.5) == "$1,234.50"


def test_format_eur():
    assert format_currency(99.9, "EUR") == "€99.90"
