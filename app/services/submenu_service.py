import aioredis
from fastapi import BackgroundTasks, Depends

from app.repository.redis_cache import AsyncRedisCache, get_async_redis_client
from app.repository.submenu import SubmenuRepository
from app.schemas.submenu import SubMenuBase


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends(),
                 redis_client: aioredis.Redis = Depends(get_async_redis_client),
                 background_tasks: BackgroundTasks = None):
        self.submenu_repository = submenu_repository
        self.cache_client = AsyncRedisCache(redis_client)
        self.background_tasks = background_tasks

    async def read_submenus(self, menu_id: int | str):
        cached = await self.cache_client.get(f'all:{menu_id}')
        if cached is not None:
            return cached

        data = await self.submenu_repository.read_submenus(menu_id)
        await self.cache_client.set(f'all:{menu_id}', data, self.background_tasks)
        return data

    async def create_submenu(self, submenu: SubMenuBase, menu_id: int | str):
        data = await self.submenu_repository.create_submenu(submenu, menu_id)
        await self.cache_client.set(f'{menu_id}:{data.id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def read_submenu(self, submenu_id: int | str, menu_id: int | str):
        cached = await self.cache_client.get(f'{menu_id}:{submenu_id}')
        if cached is not None:
            return cached

        data = await self.submenu_repository.read_submenu(submenu_id, menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}', data, self.background_tasks)
        return data

    async def update_submenu(self, submenu_id: int | str, submenu: SubMenuBase, menu_id: int | str):
        data = await self.submenu_repository.update_submenu(submenu_id, submenu, menu_id)
        await self.cache_client.set(f'{menu_id}:{submenu_id}', data, self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data

    async def del_submenu(self, submenu_id: int | str, menu_id: int | str):
        data = await self.submenu_repository.del_submenu(submenu_id, menu_id)
        await self.cache_client.delete(f'{menu_id}:{submenu_id}', self.background_tasks)
        await self.cache_client.clear_after_change(menu_id, self.background_tasks)
        return data
