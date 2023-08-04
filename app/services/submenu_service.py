import redis  # type: ignore
from fastapi import Depends

from app.repository.redis_cache import RedisCache, get_redis_client
from app.repository.submenu import SubmenuRepository
from app.schemas.submenu import SubMenuBase


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.submenu_repository = submenu_repository
        self.cache_client = RedisCache(redis_client)

    async def read_submenus(self, menu_id: int | str):
        cached = self.cache_client.get(('all', menu_id))
        if cached is not None:
            return cached
        else:
            data = await self.submenu_repository.read_submenus(menu_id)
            self.cache_client.set(('all', menu_id), data)
            return data

    async def create_submenu(self, submenu: SubMenuBase, menu_id: int | str):
        data = await self.submenu_repository.create_submenu(submenu, menu_id)
        self.cache_client.set((menu_id, data.id), data)
        self.cache_client.delete(('all', menu_id))
        return data

    async def read_submenu(self, submenu_id: int | str, menu_id: int | str):
        cached = self.cache_client.get((menu_id, submenu_id))
        if cached is not None:
            return cached
        else:
            data = await self.submenu_repository.read_submenu(submenu_id, menu_id)
            self.cache_client.set((menu_id, submenu_id), data)
            return data

    async def update_submenu(self, submenu_id: int | str, submenu: SubMenuBase, menu_id: int | str):
        data = await self.submenu_repository.update_submenu(submenu_id, submenu, menu_id)
        self.cache_client.set((menu_id, submenu_id), data)
        self.cache_client.delete(('all', menu_id))
        return data

    async def del_submenu(self, submenu_id: int | str, menu_id: int | str):
        data = await self.submenu_repository.del_submenu(submenu_id, menu_id)
        self.cache_client.delete((menu_id, submenu_id))
        self.cache_client.delete(('all', menu_id))
        return data
