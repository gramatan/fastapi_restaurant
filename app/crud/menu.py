from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.validator import validate_menu_submenu_dish
from app.database.base import Menu
from app.schemas.menu import MenuResponse, MenuBase


async def read_menus(db: AsyncSession) -> list[MenuResponse]:
    db_request = await db.execute(select(Menu))
    menus = db_request.scalars().all()
    menus_list = []
    for menu in menus:
        menu_response = MenuResponse(**menu.__dict__)
        menu_response.id = str(menu_response.id)
        menus_list.append(menu_response)
    return menus_list


async def create_menu(db: AsyncSession, menu: MenuBase) -> MenuResponse:
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return MenuResponse(**db_menu_dict)


async def read_menu(db: AsyncSession, menu_id: int) -> MenuResponse:
    menu_id = int(menu_id)
    db_menu = await validate_menu_submenu_dish(db, menu_id)
    await db.refresh(db_menu)
    menu_dict = db_menu.__dict__
    menu_dict["id"] = str(menu_dict["id"])
    return MenuResponse(**menu_dict)


async def update_menu(db: AsyncSession, menu_id: int, menu: MenuBase) -> MenuResponse:
    menu_id = int(menu_id)
    db_menu = await validate_menu_submenu_dish(db, menu_id)
    for var, value in vars(menu).items():
        setattr(db_menu, var, value) if value else None
    await db.commit()
    await db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])
    return MenuResponse(**db_menu_dict)


async def del_menu(db: AsyncSession, menu_id: int) -> dict:
    menu_id = int(menu_id)
    await validate_menu_submenu_dish(db, menu_id)
    await db.execute(delete(Menu).where(Menu.id == menu_id))
    await db.commit()
    return {"message": f"Menu {menu_id} deleted successfully."}
