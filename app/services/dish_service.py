import redis  # type: ignore
from fastapi import Depends

from app.repository.dish import DishRepository
from app.repository.redis_cache import RedisCache, get_redis_client


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.dish_repository = dish_repository
        self.cache_client = RedisCache(redis_client)

    async def read_dishes(self, submenu_id: int | str, menu_id: int | str):
        cached = self.cache_client.get(f'all:{menu_id}:{submenu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.read_dishes(submenu_id, menu_id)
            self.cache_client.set(f'all:{menu_id}:{submenu_id}', data)
            return data

    async def create_dish(self, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.create_dish(dish_data, submenu_id, menu_id)
        self.cache_client.set(f'{menu_id}:{submenu_id}:{data.id}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def read_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        cached = self.cache_client.get(f'{menu_id}:{submenu_id}:{dish_id}')
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.read_dish(dish_id, submenu_id, menu_id)
            self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data)
            return data

    async def update_dish(self, dish_id: int | str, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.update_dish(dish_id, dish_data, submenu_id, menu_id)
        self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def del_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.del_dish(dish_id, submenu_id, menu_id)
        self.cache_client.delete(f'{menu_id}:{submenu_id}:{dish_id}')
        self.cache_client.clear_after_change(menu_id)
        return data
