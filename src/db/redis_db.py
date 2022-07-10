import redis.asyncio as redis

from core.config import app_settings


connection = redis.from_url(app_settings.redis_url)


async def close_redis_connection():
    await connection.close()
