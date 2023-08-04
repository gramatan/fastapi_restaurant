
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.dish import read_dishes, create_dish, read_dish, update_dish, del_dish
from app.database.utils import get_db
from app.schemas.dish import DishResponse, DishBase

router = APIRouter()


@router.get("/dishes")
async def get_dishes(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)) -> List[DishResponse]:
    return await read_dishes(db, submenu_id, menu_id)


@router.post("/dishes", status_code=201)
async def post_dish(menu_id: int, submenu_id: int, dish: DishBase, db: AsyncSession = Depends(get_db)) -> DishResponse:
    return await create_dish(db, dish, submenu_id, menu_id)


@router.get("/dishes/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int | str, db: AsyncSession = Depends(get_db)) -> DishResponse:
    return await read_dish(db, dish_id, submenu_id, menu_id)


@router.patch("/dishes/{dish_id}")
async def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishBase, db: AsyncSession = Depends(get_db)) -> DishResponse:
    return await update_dish(db, dish_id, dish, submenu_id, menu_id)


@router.delete("/dishes/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await del_dish(db, dish_id, submenu_id, menu_id)
