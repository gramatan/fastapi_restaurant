import logging

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import DishBase, DishResponse
from app.schemas import MenuBase, MenuResponse
from app.schemas import SubMenuResponse, SubMenuBase

from app.crud import del_dish, update_dish, read_dish, create_dish, read_dishes
from app.crud import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
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
def get_menus(db: Session = Depends(get_db)) -> List[MenuResponse]:
    menus = read_menus(db)
    return menus


@app.post("/api/v1/menus", status_code=201)
def post_menu(menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    db_menu = create_menu(db, menu)
    return db_menu


@app.get("/api/v1/menus/{menu_id}")
def get_menu(menu_id: int | str, db: Session = Depends(get_db)) -> MenuResponse:
    return read_menu(db, menu_id)


@app.patch("/api/v1/menus/{menu_id}")
def patch_menu(menu_id: int, menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    return update_menu(db, menu_id, menu)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    return del_menu(db, menu_id)


# All about our Submenus.
@app.get("/api/v1/menus/{menu_id}/submenus")
def get_submenus(menu_id: int, db: Session = Depends(get_db)) -> List[SubMenuResponse]:
    submenus = read_submenus(db, menu_id)
    return submenus


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
def post_submenu(submenu: SubMenuBase, menu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    db_submenu = create_submenu(db, submenu, menu_id)
    return db_submenu


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    return read_submenu(db, submenu_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def patch_submenu(submenu_id: int, submenu: SubMenuBase, menu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
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
def post_dish(dish: DishBase, submenu_id: int, db: Session = Depends(get_db)) -> DishResponse:
    db_dish = create_dish(db, dish, submenu_id)
    return db_dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def get_dish(dish_id: int | str, db: Session = Depends(get_db)) -> DishResponse:
    return read_dish(db, dish_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def patch_dish(dish_id: int, dish: DishBase, db: Session = Depends(get_db)) -> DishResponse:
    return update_dish(db, dish_id, dish)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)) -> dict:
    return del_dish(db, dish_id)
