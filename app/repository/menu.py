from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.base import Dish, Menu, SubMenu
from app.database.utils import get_db
from app.database.validator import validate_menu_submenu_dish
from app.schemas.menu import MenuBase, MenuResponse


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.submenus_count_query = select(func.count(SubMenu.id)).where(
            SubMenu.menu_id == Menu.id).label('submenus_count')
        self.dishes_count_query = select(func.count(Dish.id)).where(Dish.submenu_id == SubMenu.id,
                                                                    SubMenu.menu_id == Menu.id).label('dishes_count')

    async def read_menus(self) -> list[MenuResponse]:
        result = await self.db.execute(
            select(Menu, self.submenus_count_query, self.dishes_count_query)
            .group_by(Menu.id)
        )
        menus_data = result.fetchall()
        return [MenuResponse(id=str(data.Menu.id), title=data.Menu.title, description=data.Menu.description,
                             submenus_count=data.submenus_count, dishes_count=data.dishes_count) for data in menus_data]

    async def create_menu(self, menu: MenuBase) -> MenuResponse:
        db_menu = Menu(**menu.model_dump())
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        return MenuResponse(id=str(db_menu.id), title=db_menu.title, description=db_menu.description,
                            submenus_count=0, dishes_count=0)

    async def read_menu(self, menu_id: int | str) -> MenuResponse:
        menu_id = int(menu_id)
        await validate_menu_submenu_dish(self.db, menu_id)
        result = await self.db.execute(
            select(Menu, self.submenus_count_query, self.dishes_count_query)
            .where(Menu.id == menu_id)
            .group_by(Menu.id)
        )
        data = result.fetchone()
        return MenuResponse(id=str(data.Menu.id), title=data.Menu.title, description=data.Menu.description,
                            submenus_count=data.submenus_count, dishes_count=data.dishes_count)

    async def update_menu(self, menu_id: int | str, menu: MenuBase) -> MenuResponse:
        menu_id = int(menu_id)
        db_menu = await validate_menu_submenu_dish(self.db, menu_id)
        for var, value in vars(menu).items():
            setattr(db_menu, var, value) if value else None
        await self.db.commit()
        await self.db.refresh(db_menu)
        result = await self.db.execute(
            select(self.submenus_count_query, self.dishes_count_query)
            .where(Menu.id == menu_id)
        )
        data = result.fetchone()
        return MenuResponse(id=str(db_menu.id), title=db_menu.title, description=db_menu.description,
                            submenus_count=data.submenus_count, dishes_count=data.dishes_count)

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

    async def get_full_menus(self):
        result = await self.db.execute(
            select(Menu).options(
                selectinload(Menu.submenus).selectinload(SubMenu.dishes)
            )
        )
        menus = result.scalars().all()

        menus_data = []
        for menu in menus:
            menu_data = {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
                'submenus': [
                    {
                        'id': submenu.id,
                        'title': submenu.title,
                        'description': submenu.description,
                        'dishes': [
                            {
                                'id': dish.id,
                                'title': dish.title,
                                'description': dish.description,
                                'price': str(dish.price)
                            } for dish in submenu.dishes
                        ]
                    } for submenu in menu.submenus
                ]
            }
            menus_data.append(menu_data)
        return menus_data
