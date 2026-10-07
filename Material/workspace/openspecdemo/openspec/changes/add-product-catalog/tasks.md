# Tasks

## 1. Project scaffold

- [x] 1.1 Add `requirements.txt` with fastapi, uvicorn, jinja2, and pytest, and verify `pip install -r requirements.txt` completes successfully
- [x] 1.2 Create the `app` package, `app/templates/`, `app/static/`, and `tests/` directories, and verify those paths exist
- [x] 1.3 Ignore `data/*.db` so the SQLite file is not committed, and verify a database path under `data/` matches the ignore rule

## 2. Seeded catalog home page

- [x] 2.1 Add `app/data/products.json` with the six design seed rows, create the SQLite `products` table, and seed it on startup when empty. Serve `GET /` so each product name is listed. Verify `test_home_page_lists_the_seeded_products` in `tests/test_product_catalog.py` passes
- [x] 2.2 On each home-page product, show the seed name, the price as Indian rupees with two decimals (for example `₹1499.00`), and the short description, using `app/static/style.css` and loading `app/static/app.js` without client-side rendering. Verify `test_listed_product_shows_name_price_and_description` passes

## 3. Product detail

- [x] 3.1 Link each home-page product name to `GET /products/{id}` and render that product's name, rupee price, and short description. Verify `test_product_detail_shows_the_selected_product` passes by following the selected product's link from the home page

## 4. Empty catalog and unknown product

- [x] 4.1 Honor `SHOPLITE_SKIP_SEED=1` and `SHOPLITE_DB` so an empty database stays empty, and show `The catalog is empty.` on the home page with no product listed. Verify `test_empty_catalog_shows_a_message` passes
- [x] 4.2 For a product id that is not in the catalog, respond with HTTP 404 and the text `Product not found.` without another product's name, price, or description. Verify `test_unknown_product_shows_not_found` passes for `/products/missing-product`

## 5. Integration

- [x] 5.1 Run the full test file and verify these scenario tests all pass: `test_home_page_lists_the_seeded_products`, `test_listed_product_shows_name_price_and_description`, `test_product_detail_shows_the_selected_product`, `test_empty_catalog_shows_a_message`, `test_unknown_product_shows_not_found`
- [x] 5.2 Start `uvicorn app.main:app --reload --port 8000` and verify the home page lists Headphones, Kettle, Notebook, Coffee Beans, USB-C Cable, and Desk Lamp
