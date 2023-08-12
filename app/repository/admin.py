from sqlalchemy import select

from app.database.base import Dish, Menu, SubMenu, async_session


async def get_menu_ids(manual_id: int) -> dict | None:
    async with async_session() as session:
        result = await session.execute(select(Menu.id).filter(Menu.manual_id == manual_id))
        menu_id = result.scalar_one_or_none()
        if menu_id:
            return {'menu_id': menu_id}
        else:
            return None


async def get_submenu_ids(manual_id: int, menu_manual_id: int) -> dict | None:

    async with async_session() as session:

        result = await session.execute(
            select(SubMenu.id, SubMenu.menu_id)
            .join(Menu, Menu.id == SubMenu.menu_id)
            .filter(SubMenu.manual_id == manual_id, Menu.manual_id == menu_manual_id)
        )
        submenu_data = result.one_or_none()

        if submenu_data:

            return {'submenu_id': submenu_data[0], 'menu_id': submenu_data[1]}

        else:

            return None


async def get_dish_ids(manual_id: int, submenu_manual_id: int, menu_manual_id: int) -> dict | None:

    async with async_session() as session:

        result = await session.execute(
            select(Dish.id, Dish.submenu_id, SubMenu.menu_id)
            .join(SubMenu, SubMenu.id == Dish.submenu_id)
            .join(Menu, Menu.id == SubMenu.menu_id)
            .filter(Dish.manual_id == manual_id, SubMenu.manual_id == submenu_manual_id,
                    Menu.manual_id == menu_manual_id)
        )

        dish_data = result.one_or_none()

        if dish_data:

            return {'dish_id': dish_data[0], 'submenu_id': dish_data[1], 'menu_id': dish_data[2]}

        else:

            return None


MenuType = list[tuple[int, str, str]]
SubMenuType = list[tuple[int, int, str, str]]
DishType = list[tuple[int, int, int, str, str, str]]


async def create_menu(menus: MenuType, manual_id: int):
    pass


async def create_submenu(submenus: SubMenuType, manual_id: int):
    pass


async def create_dish(dishes: DishType, manual_id: int):
    pass


async def update_menu(menu_id: int, menu: MenuType):
    pass


async def update_submenu(menu_id: int, submenu_id: int, submenu: SubMenuType):
    pass


async def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishType):
    pass


async def del_menu(menu_id: int):
    pass


async def del_submenu(menu_id: int, submenu_id: int):
    pass


async def del_dish(menu_id: int, submenu_id: int, dish_id: int):
    pass
