import logging

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.base import SessionLocal, Menu
from app.schemas.menu import MenuCreate, MenuUpdate, S_Menu

from app.crud import create_menu, read_menu, update_menu, read_menus, del_menu

logging.basicConfig(level=logging.INFO)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# All about our Menus:
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
    return read_menu(db, menu_id)


@app.patch("/api/v1/menus/{menu_id}")
def patch_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)) -> S_Menu:
    return update_menu(db, menu_id, menu)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    return del_menu(db, menu_id)


