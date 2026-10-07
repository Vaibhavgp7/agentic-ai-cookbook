import json
from html.parser import HTMLParser
from pathlib import Path

from fastapi.testclient import TestClient

from app.catalog import format_price
from app.main import app

SEED_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "products.json"
STATIC_DIR = Path(__file__).resolve().parents[1] / "app" / "static"


def load_seed() -> list[dict]:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[tuple[str, str]] = []
        self._href: str | None = None
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._href = dict(attrs).get("href")
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.anchors.append((self._href, "".join(self._chunks).strip()))
            self._href = None


def test_home_page_lists_the_seeded_products(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOPLITE_DB", str(tmp_path / "catalog.db"))
    monkeypatch.delenv("SHOPLITE_SKIP_SEED", raising=False)
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    for product in load_seed():
        assert product["name"] in response.text


def test_listed_product_shows_name_price_and_description(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOPLITE_DB", str(tmp_path / "catalog.db"))
    monkeypatch.delenv("SHOPLITE_SKIP_SEED", raising=False)
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    body = response.text
    assert 'href="/static/style.css"' in body
    assert 'src="/static/app.js"' in body
    script = (STATIC_DIR / "app.js").read_text(encoding="utf-8")
    assert "fetch(" not in script
    assert "innerHTML" not in script
    for product in load_seed():
        assert product["name"] in body
        assert format_price(product["price_paise"]) in body
        assert product["description"] in body


def test_product_detail_shows_the_selected_product(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOPLITE_DB", str(tmp_path / "catalog.db"))
    monkeypatch.delenv("SHOPLITE_SKIP_SEED", raising=False)
    with TestClient(app) as client:
        home = client.get("/")
        parser = AnchorParser()
        parser.feed(home.text)
        selected = next(product for product in load_seed() if product["name"] == "Headphones")
        href = next(link for link, text in parser.anchors if text == selected["name"])
        detail = client.get(href)
    assert detail.status_code == 200
    assert selected["name"] in detail.text
    assert format_price(selected["price_paise"]) in detail.text
    assert selected["description"] in detail.text


def test_empty_catalog_shows_a_message(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOPLITE_DB", str(tmp_path / "empty.db"))
    monkeypatch.setenv("SHOPLITE_SKIP_SEED", "1")
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "The catalog is empty." in response.text
    for product in load_seed():
        assert product["name"] not in response.text


def test_unknown_product_shows_not_found(tmp_path, monkeypatch):
    monkeypatch.setenv("SHOPLITE_DB", str(tmp_path / "catalog.db"))
    monkeypatch.delenv("SHOPLITE_SKIP_SEED", raising=False)
    with TestClient(app) as client:
        response = client.get("/products/missing-product")
    assert response.status_code == 404
    assert "Product not found." in response.text
    for product in load_seed():
        assert product["name"] not in response.text
        assert format_price(product["price_paise"]) not in response.text
        assert product["description"] not in response.text
