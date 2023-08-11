import pickle
from typing import Any

import aioredis
from fastapi import Depends


def get_async_redis_pool():
    return aioredis.from_url('redis://redis:6379/0', decode_responses=False)


async def get_async_redis_client(redis_pool: aioredis.Redis = Depends(get_async_redis_pool)):
    return redis_pool


class AsyncRedisCache:
    def __init__(self, redis_pool: aioredis.Redis = Depends(get_async_redis_pool)) -> None:
        self.redis_pool = redis_pool
        self.ttl = 1800

    async def get(self, key: str) -> Any | None:
        data = await self.redis_pool.get(key)
        if data is not None:
            return pickle.loads(data)
        return None

    async def set(self, key: str, value: Any) -> bool:
        data = pickle.dumps(value)
        return await self.redis_pool.setex(key, self.ttl, data)

    async def delete(self, key: str) -> int:
        return await self.redis_pool.delete(key)

    async def clear_cache(self, pattern: str):
        keys = [key async for key in self.redis_pool.scan_iter(pattern)]
        if keys:
            await self.redis_pool.delete(*keys)

    async def clear_after_change(self, menu_id: int | str):
        await self.clear_cache(f'{menu_id}*')
        await self.clear_cache('all*')
