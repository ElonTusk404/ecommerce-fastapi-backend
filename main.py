from fastapi import FastAPI
from app.api.v1.routers.category import category_router
from app.api.v1.routers.user import user_router
from app.api.v1.routers.product import product_router
from app.api.v1.routers.catalog import catalog_router
from app.api.v1.routers.cart import cart_router
from app.api.v1.routers.order import order_router
app = FastAPI()
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(order_router)

