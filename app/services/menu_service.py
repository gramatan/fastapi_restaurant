from typing import List, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.menu import MenuRepository
from app.schemas.menu import MenuResponse


class MenuService:
    def __init__(self, menu_repository: MenuRepository = Depends()):
        self.menu_repository = menu_repository

    def read_menus(self) -> List[MenuResponse]:
        return self.menu_repository.read_menus()

    def create_menu(self, menu_data):
        return self.menu_repository.create_menu(menu_data)

    def read_menu(self, menu_id: int):
        return self.menu_repository.read_menu(menu_id)

    def update_menu(self, menu_id: int, menu_data):
        return self.menu_repository.update_menu(menu_id, menu_data)

    def del_menu(self, menu_id: int):
        return self.menu_repository.del_menu(menu_id)

    def orm_read_menu(self, menu_id: int):
        return self.menu_repository.orm_read_menu(menu_id)
