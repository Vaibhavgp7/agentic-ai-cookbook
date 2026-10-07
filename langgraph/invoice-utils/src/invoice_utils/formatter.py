"""Currency formatting helpers."""


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a numeric amount as a currency string."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency + " ")
    return f"{symbol}{amount:,.2f}"
