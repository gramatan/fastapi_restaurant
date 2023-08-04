from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.validator import validate_menu_submenu_dish
from app.database.base import SubMenu
from app.database.utils import get_db
from app.schemas.submenu import SubMenuResponse, SubMenuBase


class SubmenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def read_submenus(self, menu_id: int) -> list[SubMenuResponse]:
        menu_id = int(menu_id)
        result = await self.db.execute(select(SubMenu).where(SubMenu.menu_id == menu_id))
        submenus = result.scalars().all()
        submenus_list = []
        for submenu in submenus:
            submenu_response = SubMenuResponse(**submenu.__dict__)
            submenu_response.id = str(submenu_response.id)
            submenus_list.append(submenu_response)
        return submenus_list

    async def create_submenu(self, submenu: SubMenuBase, menu_id: int) -> SubMenuResponse:
        menu_id = int(menu_id)
        db_menu = await validate_menu_submenu_dish(self.db, menu_id=menu_id)
        db_menu.submenus_count += 1
        await self.db.commit()

        db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
        self.db.add(db_submenu)
        await self.db.commit()
        await self.db.refresh(db_submenu)
        submenu_dict = db_submenu.__dict__
        submenu_dict["id"] = str(submenu_dict["id"])

        return SubMenuResponse(**submenu_dict)

    async def read_submenu(self, submenu_id: int, menu_id: int) -> SubMenuResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        submenu_dict = db_submenu.__dict__
        submenu_dict["id"] = str(submenu_dict["id"])
        return SubMenuResponse(**submenu_dict)

    async def update_submenu(self, submenu_id: int, submenu: SubMenuBase, menu_id: int) -> SubMenuResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        for var, value in vars(submenu).items():
            setattr(db_submenu, var, value) if value else None
        await self.db.commit()
        await self.db.refresh(db_submenu)
        submenu_dict = db_submenu.__dict__
        submenu_dict["id"] = str(submenu_dict["id"])
        return SubMenuResponse(**submenu_dict)

    async def del_submenu(self, submenu_id: int, menu_id: int) -> dict:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        db_menu.submenus_count -= 1
        db_menu.dishes_count -= db_submenu.dishes_count
        await self.db.commit()

        await self.db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
        await self.db.commit()
        return {"message": f"Submenu {submenu_id} deleted successfully."}
