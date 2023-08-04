import pickle
from typing import Any

import redis  # type: ignore


def get_redis_client():
    return redis.Redis(host='redis', port=6379, db=0)


class RedisCache:
    def __init__(self, redis_client: redis.Redis) -> None:
        self.redis_client = redis_client

    def get(self, key: Any) -> Any | None:
        data = self.redis_client.get(str(key))
        if data is not None:
            return pickle.loads(data)
        return None

    def set(self, key: Any, value: Any) -> bool:
        data = pickle.dumps(value)
        return self.redis_client.set(str(key), data)

    def delete(self, key: Any) -> int:
        return self.redis_client.delete(str(key))
