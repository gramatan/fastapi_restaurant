from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database.base import SubMenu
from app.schemas.submenu import SubMenuCreate, SchemasSubMenu, SubMenuUpdate
import logging


def read_submenus(db: Session, menu_id: int):
    return db.query(SubMenu).filter(SubMenu.menu_id == menu_id).all()


def create_submenu(db: Session, submenu: SubMenuCreate, menu_id: int):
    logging.info(submenu)
    db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    db_submenu_dict = db_submenu.__dict__
    db_submenu_dict["id"] = str(db_submenu_dict["id"])

    return SchemasSubMenu(**db_submenu_dict)


def read_submenu(db: Session, submenu_id: int):
    submenu = db.query(SubMenu).filter(SubMenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu.id = str(submenu.id)
    return submenu


def update_submenu(db: Session, submenu_id: int, submenu: SubMenuUpdate) -> SchemasSubMenu:
    db_submenu = db.get(SubMenu, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    for var, value in vars(submenu).items():
        setattr(db_submenu, var, value) if value else None
    db.commit()
    return db_submenu


def del_submenu(db: Session, submenu_id: int) -> dict:
    db_submenu = db.get(SubMenu, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
    db.commit()
    return {"message": f"Submenu {submenu_id} deleted successfully."}
