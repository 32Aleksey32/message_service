import redis.asyncio as aioredis

from app.settings import REDIS_BROKER_URL

redis = aioredis.from_url(REDIS_BROKER_URL)


async def redis_create_status(username: str):
    await redis.set(f"status:{username}", "online")


async def redis_get_status(username: str):
    return await redis.get(f"status:{username}")


async def redis_delete_status(username: str):
    await redis.delete(f"status:{username}")
