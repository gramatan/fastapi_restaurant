from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database.base import SubMenu, Dish
from app.schemas.submenu import SubMenuResponse, SubMenuBase
import logging


def read_submenus(db: Session, menu_id: int):
    submenus = db.query(SubMenu).filter(SubMenu.menu_id == menu_id).all()
    for submenu in submenus:
        submenu.dish_count = db.query(Dish).filter(Dish.submenu_id == submenu.id).count()
    return submenus


def create_submenu(db: Session, submenu: SubMenuBase, menu_id: int) -> SubMenuResponse:
    logging.info(submenu)
    db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


def read_submenu(db: Session, submenu_id: int) -> SubMenuResponse:
    submenu = db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_dict = submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


def update_submenu(db: Session, submenu_id: int, submenu: SubMenuBase) -> SubMenuResponse:
    db_submenu = db.get(SubMenu, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    for var, value in vars(submenu).items():
        setattr(db_submenu, var, value) if value else None
    db.commit()
    db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


def del_submenu(db: Session, submenu_id: int) -> dict:
    submenu = db.get(SubMenu, submenu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
    db.commit()
    return {"message": f"Submenu {submenu_id} deleted successfully."}
