from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.base import Menu, SubMenu, Dish


async def validate_menu_submenu_dish(db: AsyncSession, menu_id: int = None, submenu_id: int = None, dish_id: int = None):
    menu_id = int(menu_id) if menu_id is not None else None
    submenu_id = int(submenu_id) if submenu_id is not None else None
    dish_id = int(dish_id) if dish_id is not None else None
    db_menu = db_submenu = db_dish = None
    if menu_id is not None:
        db_menu = await db.get(Menu, menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail="menu not found")
    if submenu_id is not None:
        db_submenu = await db.get(SubMenu, submenu_id)
        if db_submenu is None or db_submenu.menu_id != menu_id:
            raise HTTPException(status_code=404, detail="submenu not found")
    if dish_id is not None:
        db_dish = await db.get(Dish, dish_id)
        if db_dish is None or db_dish.submenu_id != submenu_id:
            raise HTTPException(status_code=404, detail="dish not found")

    if dish_id is not None:
        return db_menu, db_submenu, db_dish
    elif submenu_id is not None:
        return db_menu, db_submenu
    elif menu_id is not None:
        return db_menu
