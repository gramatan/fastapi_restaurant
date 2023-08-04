from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.menu import read_menus, create_menu, read_menu, update_menu, del_menu, orm_read_menu
from app.database.utils import get_db
from app.schemas.menu import MenuResponse, MenuBase

router = APIRouter()


@router.get("/menus")
async def get_menus(db: AsyncSession = Depends(get_db)) -> List[MenuResponse]:
    return await read_menus(db)


@router.post("/menus", status_code=201)
async def post_menu(menu: MenuBase, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    return await create_menu(db, menu)


@router.get("/menus/{menu_id}")
async def get_menu(menu_id: int | str, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    return await read_menu(db, menu_id)


@router.patch("/menus/{menu_id}")
async def patch_menu(menu_id: int, menu: MenuBase, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    return await update_menu(db, menu_id, menu)


@router.delete("/menus/{menu_id}")
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await del_menu(db, menu_id)


@router.get("/menus/ORM/{menu_id}")
async def get_menu_orm(menu_id: int, db: AsyncSession = Depends(get_db)) -> MenuResponse:
    return await orm_read_menu(db, menu_id)
