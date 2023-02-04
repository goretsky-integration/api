from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

import v1.endpoints
import v2.endpoints
from api.errors import include_exception_handlers
from core.config import app_settings

__all__ = ('get_application',)


async def on_startup():
    redis = await aioredis.from_url(app_settings.redis_url, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(v1.endpoints.reports.router)
    app.include_router(v2.endpoints.reports.router)
    app.include_router(v1.endpoints.stop_sales.router)
    app.include_router(v2.endpoints.stop_sales.router)
    app.include_router(v1.endpoints.stocks.router)
    app.include_router(v1.endpoints.orders.router)
    include_exception_handlers(app)
    app.add_event_handler('startup', on_startup)
    return app
