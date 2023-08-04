from typing import List, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.menu import MenuRepository
from app.repository.submenu import SubmenuRepository
from app.schemas.menu import MenuResponse
from app.schemas.submenu import SubMenuBase


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends()):
        self.submenu_repository = submenu_repository

    def read_submenus(self, menu_id: int):
        return self.submenu_repository.read_submenus(menu_id)

    def create_submenu(self, submenu: SubMenuBase, menu_id: int):
        return self.submenu_repository.create_submenu(submenu, menu_id)

    def read_submenu(self, submenu_id: int, menu_id: int):
        return self.submenu_repository.read_submenu(submenu_id, menu_id)

    def update_submenu(self, submenu_id: int, submenu: SubMenuBase, menu_id: int):
        return self.submenu_repository.update_submenu(submenu_id, submenu, menu_id)

    def del_submenu(self, submenu_id: int, menu_id: int):
        return self.submenu_repository.del_submenu(submenu_id, menu_id)

