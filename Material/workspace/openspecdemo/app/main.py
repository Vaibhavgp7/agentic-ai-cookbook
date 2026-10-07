import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.catalog import format_price, get_product, list_products, seed_if_empty
from app.db import init_db

BASE_DIR = Path(__file__).resolve().parent
SEED_PATH = BASE_DIR / "data" / "products.json"
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def database_path() -> Path:
    return Path(os.environ.get("SHOPLITE_DB", "data/catalog.db"))


def skip_seed() -> bool:
    # SHOPLITE_SKIP_SEED=1 is test-only. Leave it unset so an empty database is seeded.
    return os.environ.get("SHOPLITE_SKIP_SEED") == "1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = database_path()
    init_db(path)
    if not skip_seed():
        seed_if_empty(path, SEED_PATH)
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def _with_price(product: dict) -> dict:
    priced = dict(product)
    priced["price"] = format_price(product["price_paise"])
    return priced


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    products = [_with_price(product) for product in list_products(database_path())]
    return templates.TemplateResponse(request, "home.html", {"products": products})


@app.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: str):
    product = get_product(database_path(), product_id)
    if product is None:
        return templates.TemplateResponse(
            request,
            "product.html",
            {"product": None},
            status_code=404,
        )
    return templates.TemplateResponse(
        request,
        "product.html",
        {"product": _with_price(product)},
    )
