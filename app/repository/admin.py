from sqlalchemy import select

from app.database.base import Dish, Menu, SubMenu, async_session


async def menu_exists(manual_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Menu.id).filter(Menu.manual_id == manual_id))
        return result.scalar_one_or_none() is not None


async def submenu_exists(manual_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(select(SubMenu.id).filter(SubMenu.manual_id == manual_id))
        return result.scalar_one_or_none() is not None


async def dish_exists(manual_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(select(Dish.id).filter(Dish.manual_id == manual_id))
        return result.scalar_one_or_none() is not None


MenuType = list[tuple[int, str, str]]
SubMenuType = list[tuple[int, int, str, str]]
DishType = list[tuple[int, int, int, str, str, str]]


async def create_menu(menu: MenuType, manual_id: str):
    async with async_session() as session:
        db_menu = Menu(title=menu[1], description=menu[2], manual_id=f'{manual_id}')
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        return db_menu.id


async def create_submenu(submenu: SubMenuType, manual_id: str):
    async with async_session() as session:
        db_submenu = SubMenu(title=submenu[2], description=submenu[3], menu_id=submenu[1], manual_id=manual_id)
        session.add(db_submenu)
        await session.commit()
        await session.refresh(db_submenu)
        return db_submenu.id


async def create_dish(dish: DishType, manual_id: str):
    async with async_session() as session:
        db_dish = Dish(
            title=dish[3],
            description=dish[4],
            price=dish[5],
            submenu_id=dish[1],
            manual_id=manual_id
        )
        session.add(db_dish)
        await session.commit()
        await session.refresh(db_dish)
        return db_dish.id


async def update_menu(manual_id: str, menu: MenuType):
    async with async_session() as session:
        result = await session.execute(select(Menu).filter(Menu.manual_id == manual_id))
        db_menu = result.scalar_one_or_none()
        if db_menu:
            db_menu.title = menu[1]
            db_menu.description = menu[2]
            await session.commit()
            return db_menu.manual_id


async def update_submenu(manual_id: str, submenu: SubMenuType):
    async with async_session() as session:
        result = await session.execute(select(SubMenu).filter(SubMenu.manual_id == manual_id))
        db_submenu = result.scalar_one_or_none()
        if db_submenu:
            db_submenu.title = submenu[2]
            db_submenu.description = submenu[3]
            await session.commit()
            return db_submenu.manual_id


async def update_dish(manual_id: str, dish: DishType):
    async with async_session() as session:
        result = await session.execute(select(Dish).filter(Dish.manual_id == manual_id))
        db_dish = result.scalar_one_or_none()
        if db_dish:
            db_dish.title = dish[3]
            db_dish.description = dish[4]
            db_dish.price = dish[5]
            await session.commit()
            return db_dish.manual_id


async def del_menu(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Menu).filter(Menu.manual_id == manual_id))
        db_menu = result.scalar_one_or_none()
        if db_menu:
            session.delete(db_menu)
            await session.commit()


async def del_submenu(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(SubMenu).filter(SubMenu.manual_id == manual_id))
        db_submenu = result.scalar_one_or_none()
        if db_submenu:
            session.delete(db_submenu)
            await session.commit()


async def del_dish(manual_id: str):
    async with async_session() as session:
        result = await session.execute(select(Dish).filter(Dish.manual_id == manual_id))
        db_dish = result.scalar_one_or_none()
        if db_dish:
            session.delete(db_dish)
            await session.commit()
