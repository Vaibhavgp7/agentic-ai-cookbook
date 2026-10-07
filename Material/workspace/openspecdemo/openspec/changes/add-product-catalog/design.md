# Design

## Context

The repository has no application package, database, templates, or tests. `openspec/specs/` is empty. See proposal.md for why this slice exists.

Shopper-visible behavior is in `specs/product-catalog/spec.md`. This design only records how to build that behavior within the project constraints: Python 3.11+, FastAPI, vanilla HTML/CSS/JS, SQLite, and `uvicorn app.main:app --reload --port 8000`.

## Goals / Non-Goals

**Goals:**

- Serve the catalog as server-rendered HTML from a FastAPI app.
- Seed at least the six named products into SQLite from a JSON file.
- Make the empty catalog and unknown product states reachable in tests.
- Provide one automated test per scenario, with the scenario title in the test name.

**Non-Goals:**

- A single-page app, client-side catalog rendering, or a product admin UI.
- Tables or routes for carts, accounts, or orders.
- A public JSON API. Shoppers see HTML pages.

## Decisions

### Server-rendered pages, plain links

FastAPI renders Jinja2 templates. The home page is `GET /`. Each product name is a normal link to `GET /products/{id}`. A static stylesheet in `app/static/style.css` handles layout. `app/static/app.js` is loaded so the page stack stays HTML/CSS/JS, and it does not fetch or render products.

Alternative considered: a JSON API plus browser rendering. Rejected because the spec is about pages a shopper sees, and a client renderer adds a second place for the same fields.

### SQLite seeded from JSON

Runtime catalog reads come from SQLite. The file path defaults to `data/catalog.db` and can be overridden with `SHOPLITE_DB`.

Table `products`:

- `id` TEXT primary key (stable slug)
- `name` TEXT
- `price_paise` INTEGER (Indian rupees × 100)
- `description` TEXT

On startup, if `products` is empty, load `app/data/products.json` and insert those rows. Prices render as `₹` plus two decimal places with no thousands separator (for example, `₹1499.00`).

Alternative considered: a Python seed module and no database. Rejected because this project persists data in SQLite. JSON is the seed source so the catalog can be read without executing seed logic.

Seed rows:

| id | name | price_paise | description |
| --- | --- | --- | --- |
| headphones | Headphones | 149900 | Over-ear headphones for everyday listening. |
| kettle | Kettle | 89900 | Compact electric kettle for boiling water. |
| notebook | Notebook | 24900 | Lined notebook for notes and lists. |
| coffee-beans | Coffee Beans | 59900 | Medium-roast coffee beans for home brewing. |
| usb-c-cable | USB-C Cable | 19900 | One-meter USB-C charging cable. |
| desk-lamp | Desk Lamp | 129900 | Adjustable LED lamp for a desk. |

Assumption: prices are Indian rupees. The request did not name a currency.

### Empty catalog and unknown product

`SHOPLITE_SKIP_SEED=1` skips the JSON load. Tests for the empty catalog point `SHOPLITE_DB` at a fresh database and set that flag, so startup does not refill the table. The default remains seed-on-empty.

A missing id returns HTTP 404 and the body text `Product not found.` Assumption: a detail URL for an unknown product is shopper-visible, so it has a defined message instead of a server error or another product's fields.

### Tests

Use pytest and FastAPI's `TestClient` against the HTML responses. One test function per scenario in `tests/test_product_catalog.py`. The function name contains the scenario title:

- `test_home_page_lists_the_seeded_products`
- `test_listed_product_shows_name_price_and_description`
- `test_product_detail_shows_the_selected_product`
- `test_empty_catalog_shows_a_message`
- `test_unknown_product_shows_not_found`

The home-page field test reads `app/data/products.json` and asserts each seed name, formatted price, and description is present. The detail test follows the selected product's link from the home page and checks those same three fields. The empty-catalog test uses `SHOPLITE_SKIP_SEED=1` and a temporary database. The unknown-product test requests `/products/missing-product`.

### Module layout

- `app/main.py` — FastAPI app, routes, startup seed
- `app/db.py` — SQLite connection and schema
- `app/catalog.py` — list products and get one product
- `app/data/products.json` — seed catalog
- `app/templates/home.html` — catalog list or empty message
- `app/templates/product.html` — detail or not-found message
- `app/static/style.css`, `app/static/app.js`
- `requirements.txt` — fastapi, uvicorn, jinja2, pytest
- `tests/test_product_catalog.py`

## Risks / Trade-offs

- [Skip-seed left on outside tests] → Default is unset, which seeds an empty database. Document the variable as test-only.
- [First request before seed finishes] → Seed during application startup, before routes serve traffic.
- [Currency or seed copy changes] → Keep the JSON file as the source the field test reads, and keep slugs stable so detail links do not drift.
- [Integer paise] → Avoids binary float prices. Formatting stays in one helper.

## Migration Plan

There is no existing app or database to migrate. First run creates `data/catalog.db` and loads the JSON seed. Rollback is stopping uvicorn and deleting that file.

Add `data/*.db` to `.gitignore` if a gitignore file is introduced with the app. Do not commit the database.
