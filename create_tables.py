import asyncio
import logging

from app.database.utils import create_tables, drop_tables
from app.repository.redis_cache import RedisCache, get_redis_client

logging.basicConfig(level=logging.INFO)


async def main():
    redis_client = get_redis_client()
    redis_cache = RedisCache(redis_client)

    await drop_tables()
    redis_cache.clear_cache('*')

    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())
