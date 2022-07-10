import pickle
from typing import Any

from db import redis_db
from utils import exceptions


async def set_in_cache(name: str, value: Any, expire_time: int = 60):
    obj_bytes = pickle.dumps(value)
    await redis_db.connection.set(name, obj_bytes)
    await redis_db.connection.expire(name, expire_time)


async def get_from_cache(name: str) -> Any:
    obj_bytes = await redis_db.connection.get(name)
    if obj_bytes is None:
        raise exceptions.DoesNotExistInCache(key=name)
    return pickle.loads(obj_bytes)
