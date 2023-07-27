import logging

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import async_session
from app.schemas import DishBase, DishResponse, MenuBase, MenuResponse, SubMenuResponse, SubMenuBase

from app.crud import del_dish, update_dish, read_dish, create_dish, read_dishes
from app.crud import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
from app.crud import create_menu, read_menu, update_menu, read_menus, del_menu


logging.basicConfig(level=logging.INFO)

app = FastAPI()


async def get_db():
    async with async_session() as db:
        yield db


# All about our Menus:
@app.get("/api/v1/menus")
async def get_menus(db: Session = Depends(get_db)) -> List[MenuResponse]:
    response = await read_menus(db)
    return response


@app.post("/api/v1/menus", status_code=201)
async def post_menu(menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    response = await create_menu(db, menu)
    return response


@app.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: int | str, db: Session = Depends(get_db)) -> MenuResponse:
    response = await read_menu(db, menu_id)
    return response


@app.patch("/api/v1/menus/{menu_id}")
async def patch_menu(menu_id: int, menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    response = await update_menu(db, menu_id, menu)
    return response


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    response = await del_menu(db, menu_id)
    return response


# All about our Submenus.
@app.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: int, db: Session = Depends(get_db)) -> List[SubMenuResponse]:
    submenus = await read_submenus(db, menu_id)
    return submenus


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def post_submenu(submenu: SubMenuBase, menu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    db_submenu = await create_submenu(db, submenu, menu_id)
    return db_submenu


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    response = await read_submenu(db, submenu_id)
    return response


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def patch_submenu(submenu_id: int, submenu: SubMenuBase, menu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    response = await update_submenu(db, submenu_id, submenu)
    return response


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    response = await del_submenu(db, submenu_id)
    return response


# All about our Dishes:
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(submenu_id: int, menu_id: int, db: Session = Depends(get_db)):
    dishes = await read_dishes(db, submenu_id, menu_id)
    return dishes


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def post_dish(dish: DishBase, submenu_id: int, menu_id: int, db: Session = Depends(get_db)) -> DishResponse:
    db_dish = await create_dish(db, dish, submenu_id, menu_id)
    return db_dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(dish_id: int | str, submenu_id: int, menu_id: int, db: Session = Depends(get_db)) -> DishResponse:
    response = await read_dish(db, dish_id, submenu_id, menu_id)
    return response


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def patch_dish(dish_id: int, dish: DishBase, submenu_id: int, menu_id: int, db: Session = Depends(get_db)) -> DishResponse:
    response = await update_dish(db, dish_id, dish, submenu_id, menu_id)
    return response


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(submenu_id: int, menu_id: int, dish_id: int, db: Session = Depends(get_db)) -> dict:
    response = await del_dish(db, dish_id, submenu_id, menu_id)
    return response
