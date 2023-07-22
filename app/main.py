import logging

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.crud.dish import del_dish, update_dish, read_dish, create_dish, read_dishes
from app.crud.submenu import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
from app.database.base import SessionLocal
from app.schemas.dish import DishUpdate, SchemasDish, DishCreate
from app.schemas.menu import MenuCreate, MenuUpdate, S_Menu

from app.crud import create_menu, read_menu, update_menu, read_menus, del_menu
from app.schemas.submenu import SchemasSubMenu, SubMenuUpdate, SubMenuCreate

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


# All about our Submenus:
@app.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id: int, db: Session = Depends(get_db)) -> List[SchemasSubMenu]:
    submenus = read_submenus(db, menu_id)
    return submenus


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def post_submenu(submenu: SubMenuCreate, menu_id: int, db: Session = Depends(get_db)) -> SchemasSubMenu:
    db_submenu = create_submenu(db, submenu, menu_id)
    return db_submenu


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> SchemasSubMenu:
    return read_submenu(db, submenu_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def patch_submenu(submenu_id: int, submenu: SubMenuUpdate, menu_id: int, db: Session = Depends(get_db)) -> SchemasSubMenu:
    return update_submenu(db, submenu_id, submenu)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return del_submenu(db, submenu_id)


# All about our Dishes:
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
def get_dishes(db: Session = Depends(get_db)):
    dishes = read_dishes(db)
    return dishes


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
def post_dish(dish: DishCreate, db: Session = Depends(get_db)) -> SchemasDish:
    db_dish = create_dish(db, dish)
    return db_dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(dish_id: int | str, db: Session = Depends(get_db)):
    return read_dish(db, dish_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def patch_dish(dish_id: int, dish: DishUpdate, db: Session = Depends(get_db)) -> SchemasDish:
    return update_dish(db, dish_id, dish)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    return del_dish(db, dish_id)
