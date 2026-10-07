# Spec Delta

## Purpose

Lets a shopper browse ShopLite's product catalog and open a product to see its name, price, and short description.

## ADDED Requirements

### Requirement: Home page lists the seeded catalog
The home page SHALL list every product in the catalog. The seeded catalog SHALL include at least these six everyday products: Headphones, Kettle, Notebook, Coffee Beans, USB-C Cable, and Desk Lamp.

#### Scenario: Home page lists the seeded products
- **WHEN** a shopper opens the home page and the seeded catalog is available
- **THEN** the page lists Headphones, Kettle, Notebook, Coffee Beans, USB-C Cable, and Desk Lamp

### Requirement: Listed product shows name, price, and description
Each product listed on the home page SHALL show its name, its price in Indian rupees, and a short description.

#### Scenario: Listed product shows name price and description
- **WHEN** a shopper views a product on the home page
- **THEN** that product shows its name, its price in Indian rupees, and a short description

### Requirement: Product detail shows the selected product
Selecting a product SHALL open a detail page for that product. The detail page SHALL show the same name, price in Indian rupees, and short description as the catalog entry.

#### Scenario: Product detail shows the selected product
- **WHEN** a shopper selects a product from the home page
- **THEN** a detail page shows that product's name, price in Indian rupees, and short description

### Requirement: Empty catalog shows a message
When the catalog contains no products, the home page SHALL show the message "The catalog is empty." and SHALL list no products.

#### Scenario: Empty catalog shows a message
- **WHEN** a shopper opens the home page and the catalog contains no products
- **THEN** the page shows "The catalog is empty." and lists no products

### Requirement: Unknown product shows not found
When a shopper requests a product that is not in the catalog, the page SHALL show the message "Product not found." and SHALL NOT show another product's name, price, or description.

#### Scenario: Unknown product shows not found
- **WHEN** a shopper opens the detail page for a product that is not in the catalog
- **THEN** the page shows "Product not found." and does not show another product's name, price, or description
