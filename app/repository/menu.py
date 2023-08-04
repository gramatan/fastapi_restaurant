from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Dish, Menu, SubMenu
from app.database.utils import get_db
from app.database.validator import validate_menu_submenu_dish
from app.schemas.menu import MenuBase, MenuResponse


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def read_menus(self) -> list[MenuResponse]:
        db_request = await self.db.execute(select(Menu))
        menus = db_request.scalars().all()
        menus_list: list[MenuResponse] = list()
        for menu in menus:
            menu_response = MenuResponse(**menu.__dict__)
            menu_response.id = str(menu_response.id)
            menus_list.append(menu_response)
        return menus_list

    async def create_menu(self, menu: MenuBase) -> MenuResponse:
        db_menu = Menu(**menu.model_dump())
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        db_menu_dict = db_menu.__dict__
        db_menu_dict['id'] = str(db_menu_dict['id'])

        return MenuResponse(**db_menu_dict)

    async def read_menu(self, menu_id: int | str) -> MenuResponse:
        menu_id = int(menu_id)
        db_menu = await validate_menu_submenu_dish(self.db, menu_id)
        await self.db.refresh(db_menu)
        menu_dict = db_menu.__dict__
        menu_dict['id'] = str(menu_dict['id'])
        return MenuResponse(**menu_dict)

    async def update_menu(self, menu_id: int | str, menu: MenuBase) -> MenuResponse:
        menu_id = int(menu_id)
        db_menu = await validate_menu_submenu_dish(self.db, menu_id)
        for var, value in vars(menu).items():
            setattr(db_menu, var, value) if value else None
        await self.db.commit()
        await self.db.refresh(db_menu)
        db_menu_dict = db_menu.__dict__
        db_menu_dict['id'] = str(db_menu_dict['id'])
        return MenuResponse(**db_menu_dict)

    async def del_menu(self, menu_id: int | str) -> dict:
        menu_id = int(menu_id)
        await validate_menu_submenu_dish(self.db, menu_id)
        await self.db.execute(delete(Menu).where(Menu.id == menu_id))
        await self.db.commit()
        return {'message': f'Menu {menu_id} deleted successfully.'}

    async def orm_read_menu(self, menu_id: int | str):
        menu_id = int(menu_id)
        await validate_menu_submenu_dish(self.db, menu_id)

        submenus_count = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu_id)
        dishes_count = select(func.count(Dish.id)).where(Dish.submenu_id == SubMenu.id, SubMenu.menu_id == menu_id)

        result = await self.db.execute(
            select(Menu, submenus_count.label('submenus_count'), dishes_count.label('dishes_count'))
            .where(Menu.id == menu_id)
        )

        row = result.one()

        menu, submenus_count, dishes_count = row

        menu_dict = {key: value for key, value in menu.__dict__.items() if not key.startswith('_')}
        menu_dict['id'] = str(menu_dict['id'])

        menu_dict['submenus_count'] = submenus_count
        menu_dict['dishes_count'] = dishes_count

        return menu_dict
