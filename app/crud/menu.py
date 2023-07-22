from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database import Menu
from app.schemas import MenuResponse, MenuBase
import logging


def read_menus(db: Session) -> list[MenuResponse]:
    menus = db.query(Menu).all()
    menus_list = []
    for menu in menus:
        menu_response = MenuResponse(**menu.__dict__)
        menu_response.id = str(menu_response.id)
        menus_list.append(menu_response)
    return menus_list


def create_menu(db: Session, menu: MenuBase) -> MenuResponse:
    logging.info(menu)
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return MenuResponse(**db_menu_dict)


def read_menu(db: Session, menu_id: int) -> MenuResponse:
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db.refresh(db_menu)
    menu_dict = db_menu.__dict__
    menu_dict["id"] = str(menu_dict["id"])
    return MenuResponse(**menu_dict)


def update_menu(db: Session, menu_id: int, menu: MenuBase) -> MenuResponse:
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    for var, value in vars(menu).items():
        setattr(db_menu, var, value) if value else None
    db.commit()
    db.refresh(db_menu)
    db_menu_dict = db_menu.__dict__
    db_menu_dict["id"] = str(db_menu_dict["id"])

    return MenuResponse(**db_menu_dict)


def del_menu(db: Session, menu_id: int) -> dict:
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db.execute(delete(Menu).where(Menu.id == menu_id))
    db.commit()
    return {"message": f"Menu {menu_id} deleted successfully."}
