from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

import api
from core.config import app_settings

__all__ = ('get_application',)


async def on_startup():
    redis = await aioredis.from_url(app_settings.redis_url, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api.v1.reports.router)
    app.include_router(api.v1.orders.router)
    app.include_router(api.v1.stocks.router)
    app.include_router(api.v1.stop_sales.router)
    app.include_router(api.v2.reports.router)
    app.include_router(api.v2.stop_sales.router)
    api.errors.include_exception_handlers(app)
    app.add_event_handler('startup', on_startup)
    return app
