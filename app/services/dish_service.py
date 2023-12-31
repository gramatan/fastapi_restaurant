import redis.asyncio as redis  # type: ignore
from fastapi import BackgroundTasks, Depends

from app.repository.dish import DishRepository
from app.repository.redis_cache import AsyncRedisCache, get_async_redis_client


class DishService:
    def __init__(self,
                 dish_repository: DishRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_async_redis_client),
                 background_tasks: BackgroundTasks = None):
        self.dish_repository = dish_repository
        self.cache_client = AsyncRedisCache(redis_client)
        self.background_tasks = background_tasks

    async def read_dishes(self, submenu_id: int | str, menu_id: int | str):
        cached = await self.cache_client.get(f'all:{menu_id}:{submenu_id}')
        if cached is not None:
            return cached

        data = await self.dish_repository.read_dishes(submenu_id, menu_id)
        await self.cache_client.set(f'all:{menu_id}:{submenu_id}', data, self.background_tasks)
        return data

    async def create_dish(self, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.create_dish(dish_data, submenu_id, menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}:{data.id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def read_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        cached = await self.cache_client.get(f'{menu_id}:{submenu_id}:{dish_id}')
        if cached is not None:
            return cached

        data = await self.dish_repository.read_dish(dish_id, submenu_id, menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data, self.background_tasks)
        return data

    async def update_dish(self, dish_id: int | str, dish_data, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.update_dish(dish_id, dish_data, submenu_id, menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}:{dish_id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def del_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        data = await self.dish_repository.del_dish(dish_id, submenu_id, menu_id)
        await self.cache_client.delete(f'{menu_id}:{submenu_id}:{dish_id}', self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data
