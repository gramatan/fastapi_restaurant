import asyncio
import logging

import redis  # type: ignore

from app.database.utils import create_tables, drop_tables

logging.basicConfig(level=logging.INFO)


def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)


class RedisCache:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client
        self.ttl = 1800

    def clear_cache(self, pattern: str):
        for key in self.redis_client.scan_iter(pattern):
            self.redis_client.delete(key)


async def main():
    redis_client = get_redis_client()
    redis_cache = RedisCache(redis_client)

    await drop_tables()
    redis_cache.clear_cache('*')

    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())
