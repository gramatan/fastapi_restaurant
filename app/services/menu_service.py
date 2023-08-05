import redis  # type: ignore
from fastapi import Depends

from app.repository.menu import MenuRepository
from app.repository.redis_cache import RedisCache, get_redis_client


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends(),
                 redis_client: redis.Redis = Depends(get_redis_client)):
        self.menu_repository = menu_repository
        self.cache_client = RedisCache(redis_client)

    async def read_menus(self):
        cached = self.cache_client.get('all')
        if cached is not None:
            return cached
        else:
            data = await self.menu_repository.read_menus()
            self.cache_client.set('all', data)
            return data

    async def create_menu(self, menu_data):
        data = await self.menu_repository.create_menu(menu_data)
        self.cache_client.set(f'{data.id}', data)
        self.cache_client.clear_after_change(data.id)
        return data

    async def read_menu(self, menu_id: int | str):
        cached = self.cache_client.get(f'{menu_id}')
        if cached is not None:
            return cached
        else:
            data = await self.menu_repository.read_menu(menu_id)
            self.cache_client.set(f'{menu_id}', data)
            return data

    async def update_menu(self, menu_id: int | str, menu_data):
        data = await self.menu_repository.update_menu(menu_id, menu_data)
        self.cache_client.set(f'{menu_id}', data)
        self.cache_client.clear_after_change(menu_id)
        return data

    async def del_menu(self, menu_id: int | str):
        data = await self.menu_repository.del_menu(menu_id)
        self.cache_client.delete(f'{menu_id}')
        self.cache_client.clear_after_change(menu_id)
        return data

    async def orm_read_menu(self, menu_id: int | str):
        return await self.menu_repository.orm_read_menu(menu_id)
