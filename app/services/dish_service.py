import redis  # type: ignore
from fastapi import Depends

from app.repository.dish import DishRepository
from app.repository.redis_cache import get_redis_client


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.dish_repository = dish_repository
        self.cache_client = redis_client

    async def read_dishes(self, submenu_id: int | str, menu_id: int | str):
        cached = self.cache_client.get(('all', submenu_id, menu_id))
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.read_dishes(submenu_id, menu_id)
            self.cache_client.set(('all', submenu_id, menu_id), data)
            return data

    async def create_dish(self, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.create_dish(dish_data, submenu_id, menu_id)
        self.cache_client.set((submenu_id, menu_id, data.id), data)
        self.clear_cache_lists(submenu_id, menu_id)
        return data

    async def read_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        cached = self.cache_client.get((submenu_id, menu_id, dish_id))
        if cached is not None:
            return cached
        else:
            data = await self.dish_repository.read_dish(dish_id, submenu_id, menu_id)
            self.cache_client.set((submenu_id, menu_id, dish_id), data)
            return data

    async def update_dish(self, dish_id: int | str, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.update_dish(dish_id, dish_data, submenu_id, menu_id)
        self.cache_client.set((submenu_id, menu_id, dish_id), data)
        self.clear_cache_lists(submenu_id, menu_id)
        return data

    async def del_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.del_dish(dish_id, submenu_id, menu_id)
        self.cache_client.delete((submenu_id, menu_id, dish_id))
        self.clear_cache_lists(submenu_id, menu_id)
        return data

    def clear_cache_lists(self, submenu_id: int | str, menu_id: int | str):
        self.cache_client.delete(('all', submenu_id, menu_id))
        self.cache_client.delete(('all', menu_id))
