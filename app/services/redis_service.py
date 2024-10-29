import json
import uuid
from typing import List
from uuid import UUID

import redis.asyncio as aioredis

from app.settings import CACHE_EXPIRE_MINUTES, REDIS_EXPIRE_MINUTES, REDIS_URL

redis = aioredis.from_url(REDIS_URL)


async def redis_create_status(username: str):
    await redis.set(f"status:{username}", "online")


async def redis_get_status(username: str):
    return await redis.get(f"status:{username}")


async def redis_delete_status(username: str):
    await redis.delete(f"status:{username}")


async def redis_create_session(user_id: UUID):
    session_id = str(uuid.uuid4())
    ex_seconds = REDIS_EXPIRE_MINUTES * 60
    await redis.set(f"session:{session_id}", str(user_id), ex=ex_seconds)
    return session_id


async def redis_get_session(session_id: str):
    user_id = await redis.get(f"session:{session_id}")
    if user_id:
        user_id = user_id.decode('utf-8')
        return uuid.UUID(user_id)


async def redis_delete_session(session_id: str):
    await redis.delete(session_id)


async def redis_set_cache(key: str, data: List[dict]):
    ex_seconds = CACHE_EXPIRE_MINUTES * 60
    await redis.setex(key, ex_seconds, json.dumps(data))


async def redis_get_cache(key: str):
    cached_data = await redis.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None


async def redis_delete_cache(key: str):
    await redis.delete(key)
