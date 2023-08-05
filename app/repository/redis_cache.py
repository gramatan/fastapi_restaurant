import pickle
from typing import Any

import redis  # type: ignore


def get_redis_client():
    return redis.Redis(host='redis', port=6379, db=0)


class RedisCache:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client
        self.ttl = 1800

    def get(self, key: str) -> Any | None:
        data = self.redis_client.get(key)
        if data is not None:
            return pickle.loads(data)
        return None

    def set(self, key: str, value: Any) -> bool:
        data = pickle.dumps(value)
        return self.redis_client.setex(key, self.ttl, data)

    def delete(self, key: str) -> int:
        return self.redis_client.delete(key)

    def clear_cache(self, pattern: str):
        for key in self.redis_client.scan_iter(pattern):
            self.redis_client.delete(key)

    def clear_after_change(self, menu_id: int | str):
        self.clear_cache(f'{menu_id}*')
        self.clear_cache('all*')
