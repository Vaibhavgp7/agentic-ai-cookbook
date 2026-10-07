import json
from pathlib import Path

from app.db import connect


def format_price(price_paise: int) -> str:
    rupees, paise = divmod(int(price_paise), 100)
    return f"₹{rupees}.{paise:02d}"


def seed_if_empty(db_path: Path, seed_path: Path) -> None:
    products = json.loads(seed_path.read_text(encoding="utf-8"))
    with connect(db_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count:
            return
        connection.executemany(
            """
            INSERT INTO products (id, name, price_paise, description)
            VALUES (?, ?, ?, ?)
            """,
            [
                (item["id"], item["name"], item["price_paise"], item["description"])
                for item in products
            ],
        )


def list_products(db_path: Path) -> list[dict]:
    with connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, name, price_paise, description
            FROM products
            ORDER BY name
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_product(db_path: Path, product_id: str) -> dict | None:
    with connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT id, name, price_paise, description
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()
    if row is None:
        return None
    return dict(row)
