from typing import Annotated, List
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from app.api.v1.routers.category import category_router
from app.api.v1.routers.user import user_router
from app.api.v1.routers.product import product_router
from app.api.v1.routers.catalog import catalog_router
from app.api.v1.routers.cart import cart_router
from app.api.v1.routers.order import order_router
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #ONLY IN DEV
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(order_router)

