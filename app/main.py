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
    return await read_menus(db)


@app.post("/api/v1/menus", status_code=201)
async def post_menu(menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    return await create_menu(db, menu)


@app.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: int | str, db: Session = Depends(get_db)) -> MenuResponse:
    return await read_menu(db, menu_id)


@app.patch("/api/v1/menus/{menu_id}")
async def patch_menu(menu_id: int, menu: MenuBase, db: Session = Depends(get_db)) -> MenuResponse:
    return await update_menu(db, menu_id, menu)


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int, db: Session = Depends(get_db)) -> dict:
    return await del_menu(db, menu_id)


# All about our Submenus.
@app.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus(menu_id: int, db: Session = Depends(get_db)) -> List[SubMenuResponse]:
    return await read_submenus(db, menu_id)


@app.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def post_submenu(submenu: SubMenuBase, menu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    return await create_submenu(db, submenu, menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> SubMenuResponse:
    return await read_submenu(db, submenu_id, menu_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def patch_submenu(menu_id: int, submenu_id: int, submenu: SubMenuBase, db: Session = Depends(get_db)) -> SubMenuResponse:
    return await update_submenu(db, submenu_id, submenu, menu_id)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> dict:
    return await del_submenu(db, submenu_id, menu_id)


# All about our Dishes:
@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)) -> List[DishResponse]:
    return await read_dishes(db, submenu_id, menu_id)


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def post_dish(menu_id: int, submenu_id: int, dish: DishBase, db: Session = Depends(get_db)) -> DishResponse:
    return await create_dish(db, dish, submenu_id, menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int | str, db: Session = Depends(get_db)) -> DishResponse:
    return await read_dish(db, dish_id, submenu_id, menu_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishBase, db: Session = Depends(get_db)) -> DishResponse:
    return await update_dish(db, dish_id, dish, submenu_id, menu_id)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)) -> dict:
    return await del_dish(db, dish_id, submenu_id, menu_id)
