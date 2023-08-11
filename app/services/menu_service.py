import aioredis
from fastapi import BackgroundTasks, Depends

from app.repository.menu import MenuRepository
from app.repository.redis_cache import AsyncRedisCache, get_async_redis_client


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends(),
                 redis_client: aioredis.Redis = Depends(get_async_redis_client),
                 background_tasks: BackgroundTasks = None):
        self.menu_repository = menu_repository
        self.cache_client = AsyncRedisCache(redis_client)
        self.background_tasks = background_tasks

    async def read_menus(self):
        cached = await self.cache_client.get('all')
        if cached is not None:
            return cached

        data = await self.menu_repository.read_menus()
        await self.cache_client.set('all', data, self.background_tasks)
        return data

    async def create_menu(self, menu_data):
        data = await self.menu_repository.create_menu(menu_data)
        await self.cache_client.set(f'{data.id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(data.id, self.background_tasks)
        return data

    async def read_menu(self, menu_id: int | str):
        cached = await self.cache_client.get(f'{menu_id}')
        if cached is not None:
            return cached

        data = await self.menu_repository.read_menu(menu_id)
        await self.cache_client.set(f'{menu_id}', data, self.background_tasks)
        return data

    async def update_menu(self, menu_id: int | str, menu_data):
        data = await self.menu_repository.update_menu(menu_id, menu_data)
        await self.cache_client.set(f'{menu_id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def del_menu(self, menu_id: int | str):
        data = await self.menu_repository.del_menu(menu_id)
        await self.cache_client.delete(f'{menu_id}', self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def orm_read_menu(self, menu_id: int | str):
        return await self.menu_repository.orm_read_menu(menu_id)
