from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database.base import Menu, SubMenu, Dish
from app.schemas.menu import MenuCreate, S_Menu, MenuUpdate
import logging


def read_menus(db: Session):
    menus = db.query(Menu).all()
    for menu in menus:
        menu.submenu_count = db.query(SubMenu).filter(SubMenu.menu_id == menu.id).count()
        menu.dish_count = db.query(Dish).join(SubMenu).filter(SubMenu.menu_id == menu.id).count()
    return menus


def create_menu(db: Session, menu: MenuCreate):
    logging.info(menu)
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return S_Menu(**db_menu_dict)


def read_menu(db: Session, menu_id: int):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    menu.id = str(menu.id)
    return menu


# Для update_menu:
def update_menu(db: Session, menu_id: int, menu: MenuUpdate) -> S_Menu:
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    for var, value in vars(menu).items():
        setattr(db_menu, var, value) if value else None
    db.commit()
    return db_menu

# Для del_menu:
def del_menu(db: Session, menu_id: int) -> dict:
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db.execute(delete(Menu).where(Menu.id == menu_id))
    db.commit()
    return {"message": f"Menu {menu_id} deleted successfully."}

