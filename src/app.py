from fastapi import FastAPI, status, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

import v1.endpoints
import v2.endpoints
from core.config import app_settings

__all__ = (
    'app',
)

app = FastAPI()
app.include_router(v1.endpoints.reports.router)
app.include_router(v2.endpoints.reports.router)
app.include_router(v1.endpoints.stop_sales.router)
app.include_router(v2.endpoints.stop_sales.router)
app.include_router(v1.endpoints.stocks.router)
app.include_router(v1.endpoints.orders.router)


@app.get('/ping')
async def ping():
    return Response(status_code=status.HTTP_200_OK)


@app.on_event('startup')
async def on_startup():
    redis = await aioredis.from_url(app_settings.redis_url, encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
