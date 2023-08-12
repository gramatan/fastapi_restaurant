from sqlalchemy import select

from app.database.base import Dish, Menu, SubMenu, async_session

MenuType = list[tuple[int, str, str]]
SubMenuType = list[tuple[int, int, str, str]]
DishType = list[tuple[int, int, int, str, str, str]]


async def create_update_menu(menu: MenuType, manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Menu).filter(Menu.manual_id == manual_id))
        db_menu = result.scalar_one_or_none()

        if db_menu:
            db_menu.title = menu[1]
            db_menu.description = menu[2]
            await session.commit()
        else:
            db_menu = Menu(title=menu[1], description=menu[2], manual_id=f'{manual_id}')
            session.add(db_menu)
            await session.commit()
            await session.refresh(db_menu)
        return manual_id, menu[1], menu[2]


async def create_update_submenu(submenu: SubMenuType, manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(SubMenu).filter(SubMenu.manual_id == manual_id))
        db_submenu = result.scalar_one_or_none()

        menu_manual_id = manual_id.rsplit(':', 1)[0]
        menu_id_result = await session.execute(select(Menu.id).filter(Menu.manual_id == menu_manual_id))
        menu_id = menu_id_result.scalar_one_or_none()

        if db_submenu:
            db_submenu.title = submenu[2]
            db_submenu.description = submenu[3]
            await session.commit()
        else:
            new_submenu = SubMenu(title=submenu[2], description=submenu[3], menu_id=menu_id, manual_id=manual_id)
            session.add(new_submenu)
            await session.commit()
            await session.refresh(new_submenu)
        return manual_id, submenu[2], submenu[3]


async def create_update_dish(dish: DishType, manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Dish).filter(Dish.manual_id == manual_id))
        db_dish = result.scalar_one_or_none()

        submenu_manual_id = manual_id.rsplit(':', 1)[0]
        submenu_id_result = await session.execute(select(SubMenu.id).filter(SubMenu.manual_id == submenu_manual_id))
        submenu_id = submenu_id_result.scalar_one_or_none()

        if db_dish:
            db_dish.title = dish[3]
            db_dish.description = dish[4]
            db_dish.price = dish[5]
            await session.commit()
        else:
            new_dish = Dish(title=dish[3], description=dish[4], price=dish[5],
                            submenu_id=submenu_id, manual_id=manual_id)
            session.add(new_dish)
            await session.commit()
            await session.refresh(new_dish)
        return manual_id, dish[3], dish[4], dish[5]


async def check_and_del_menu(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Menu).filter(Menu.manual_id == manual_id))
        db_menu = result.scalar_one_or_none()
        if db_menu:
            await session.delete(db_menu)
            await session.commit()


async def check_and_del_submenu(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(SubMenu).filter(SubMenu.manual_id == manual_id))
        db_submenu = result.scalar_one_or_none()
        if db_submenu:
            await session.delete(db_submenu)
            await session.commit()


async def check_and_del_dish(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Dish).filter(Dish.manual_id == manual_id))
        db_dish = result.scalar_one_or_none()
        if db_dish:
            await session.delete(db_dish)
            await session.commit()
