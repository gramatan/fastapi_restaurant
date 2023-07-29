from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.validator import validate_menu_submenu_dish
from app.database.base import Menu, SubMenu, Dish


async def orm_read_menu(db: AsyncSession, menu_id: int):
    menu_id = int(menu_id)
    await validate_menu_submenu_dish(db, menu_id)

    submenus_count = select(func.count(SubMenu.id)).where(SubMenu.menu_id == menu_id)
    dishes_count = select(func.count(Dish.id)).where(Dish.submenu_id == SubMenu.id, SubMenu.menu_id == menu_id)

    result = await db.execute(
        select(Menu, submenus_count.label("submenus_count"), dishes_count.label("dishes_count"))
        .where(Menu.id == menu_id)
    )

    row = result.one()

    menu, submenus_count, dishes_count = row

    menu_dict = {key: value for key, value in menu.__dict__.items() if not key.startswith('_')}
    menu_dict["id"] = str(menu_dict["id"])

    menu_dict['submenus_count'] = submenus_count
    menu_dict['dishes_count'] = dishes_count

    return menu_dict
