import logging

from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.calc_submenu_and_dishes import orm_read_menu
from app.database.utils import get_db
from app.routers import menu_router
from app.schemas.menu import MenuBase, MenuResponse
from app.schemas.submenu import SubMenuBase, SubMenuResponse
from app.schemas.dish import DishBase, DishResponse

from app.crud.dish import del_dish, update_dish, read_dish, create_dish, read_dishes
from app.crud.submenu import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
from app.crud.menu import create_menu, read_menu, update_menu, read_menus, del_menu


logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(menu_router.router, prefix="/api/v1/menus", tags=["menus"])


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

