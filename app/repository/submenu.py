from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Dish, SubMenu
from app.database.utils import get_db
from app.database.validator import validate_menu_submenu_dish
from app.schemas.submenu import SubMenuBase, SubMenuResponse


class SubmenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.dishes_count_query = select(func.count(Dish.id)).where(Dish.submenu_id == SubMenu.id).label('dishes_count')

    async def read_submenus(self, menu_id: int | str) -> list[SubMenuResponse]:
        menu_id = int(menu_id)
        result = await self.db.execute(
            select(SubMenu, self.dishes_count_query)
            .where(SubMenu.menu_id == menu_id)
            .group_by(SubMenu.id)
        )
        submenus_data = result.fetchall()
        return [SubMenuResponse(id=str(data.SubMenu.id), title=data.SubMenu.title, description=data.SubMenu.description,
                                dishes_count=data.dishes_count) for data in submenus_data]

    async def create_submenu(self, submenu: SubMenuBase, menu_id: int | str) -> SubMenuResponse:
        menu_id = int(menu_id)
        db_menu = await validate_menu_submenu_dish(self.db, menu_id=menu_id)
        db_menu.submenus_count += 1
        await self.db.commit()

        db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
        self.db.add(db_submenu)
        await self.db.commit()
        await self.db.refresh(db_submenu)
        submenu_dict = db_submenu.__dict__
        submenu_dict['id'] = str(submenu_dict['id'])

        return SubMenuResponse(id=str(db_submenu.id), title=db_submenu.title,
                               description=db_submenu.description, dishes_count=0)

    async def read_submenu(self, submenu_id: int | str, menu_id: int | str) -> SubMenuResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        result = await self.db.execute(
            select(SubMenu, self.dishes_count_query)
            .where(SubMenu.id == submenu_id)
            .group_by(SubMenu.id)
        )
        data = result.fetchone()
        return SubMenuResponse(id=str(data.SubMenu.id), title=data.SubMenu.title, description=data.SubMenu.description,
                               dishes_count=data.dishes_count)

    async def update_submenu(self, submenu_id: int | str, submenu: SubMenuBase, menu_id: int | str) -> SubMenuResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        for var, value in vars(submenu).items():
            setattr(db_submenu, var, value) if value else None
        await self.db.commit()
        await self.db.refresh(db_submenu)
        result = await self.db.execute(
            select(self.dishes_count_query)
            .where(SubMenu.id == submenu_id)
        )
        data = result.fetchone()
        return SubMenuResponse(id=str(db_submenu.id), title=db_submenu.title, description=db_submenu.description,
                               dishes_count=data.dishes_count)

    async def del_submenu(self, submenu_id: int | str, menu_id: int | str) -> dict:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id=menu_id, submenu_id=submenu_id)
        db_menu.submenus_count -= 1
        db_menu.dishes_count -= db_submenu.dishes_count
        await self.db.commit()

        await self.db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
        await self.db.commit()
        return {'message': f'Submenu {submenu_id} deleted successfully.'}
