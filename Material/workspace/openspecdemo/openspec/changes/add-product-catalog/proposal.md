# Proposal

## Why

ShopLite has no storefront yet, so a shopper cannot see what Nile Retail sells. A small product catalog is the first slice a later cart and checkout can build on.

## What Changes

- Add a home page that lists the seeded catalog (at least six everyday products).
- Show each product's name, price, and a short description on the home page.
- Open a product detail page with the same fields when a shopper selects a product.
- Show a clear empty-catalog message when the product list has no items.
- Seed the catalog; do not add search, cart, checkout, accounts, recommendations, payments, or inventory rules.

## Capabilities

### New Capabilities

- `product-catalog`: A shopper can browse the seeded catalog on the home page and open a product to see its name, price, and short description, including the empty-catalog case.

### Modified Capabilities

- None.

## Impact

- New FastAPI application (`app.main:app`) served with uvicorn on port 8000, using vanilla HTML, CSS, and JavaScript.
- New product seed data and a SQLite store for the catalog.
- New automated tests, one per shopper-visible scenario, with the scenario title in the test name.
- No existing APIs, pages, or specs to change.
