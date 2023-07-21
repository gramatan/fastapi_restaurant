import logging

from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.database.base import SessionLocal, Menu
from app.schemas.menu import MenuCreate, MenuUpdate, S_Menu

from app.crud import create_menu, read_menu, update_menu, delete_menu, read_menus

logging.basicConfig(level=logging.INFO)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus")
def get_menus(db: Session = Depends(get_db)) -> List[S_Menu]:
    menus = read_menus(db)
    return menus


@app.post("/api/v1/menus", status_code=201)
def post_menu(menu: MenuCreate, db: Session = Depends(get_db)) -> S_Menu:
    db_menu = create_menu(db, menu)
    return db_menu

@app.get("/api/v1/menus/{menu_id}")
def get_menu(menu_id: int | str, db: Session = Depends(get_db)) -> S_Menu:
    menu = read_menu(db, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    menu.id = str(menu.id)
    return menu

@app.patch("/api/v1/menus/{menu_id}")
def patch_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)) -> S_Menu:
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    for var, value in vars(menu).items():
        setattr(db_menu, var, value) if value else None
    db.commit()
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.execute(delete(Menu).where(Menu.id == menu_id))
    db.commit()
    return {"message": f"Menu {menu_id} deleted successfully."}



