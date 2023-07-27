from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.database import Menu
from app.schemas import MenuResponse, MenuBase
import logging


async def read_menus(db: Session) -> list[MenuResponse]:
    db_request = await db.execute(select(Menu))
    menus = db_request.scalars().all()
    menus_list = []
    for menu in menus:
        menu_response = MenuResponse(**menu.__dict__)
        menu_response.id = str(menu_response.id)
        menus_list.append(menu_response)
    return menus_list


async def create_menu(db: Session, menu: MenuBase) -> MenuResponse:
    logging.info(menu)
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return MenuResponse(**db_menu_dict)


async def read_menu(db: Session, menu_id: int) -> MenuResponse:
    db_menu = await db.get(Menu, int(menu_id))
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    await db.refresh(db_menu)
    menu_dict = db_menu.__dict__
    menu_dict["id"] = str(menu_dict["id"])
    return MenuResponse(**menu_dict)


async def update_menu(db: Session, menu_id: int, menu: MenuBase) -> MenuResponse:
    db_menu = await db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    for var, value in vars(menu).items():
        setattr(db_menu, var, value) if value else None
    await db.commit()
    await db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return MenuResponse(**db_menu_dict)


async def del_menu(db: Session, menu_id: int) -> dict:
    db_menu = await db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    await db.execute(delete(Menu).where(Menu.id == menu_id))
    await db.commit()
    return {"message": f"Menu {menu_id} deleted successfully."}
