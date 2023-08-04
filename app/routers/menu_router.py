from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.menu import read_menus, create_menu, read_menu, update_menu, del_menu, orm_read_menu
from app.database.utils import get_db
from app.schemas.menu import MenuResponse, MenuBase
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("/menus", response_model=List[MenuResponse])
async def get_menus(response: MenuService = Depends()):
    return await response.read_menus()


@router.post("/menus", status_code=201)
async def post_menu(menu: MenuBase, response: MenuService = Depends()) -> MenuResponse:
    return await response.create_menu(menu)


@router.get("/menus/{menu_id}")
async def get_menu(menu_id: int | str, response: MenuService = Depends()) -> MenuResponse:
    return await response.read_menu(menu_id)


@router.patch("/menus/{menu_id}")
async def patch_menu(menu_id: int, menu: MenuBase, response: MenuService = Depends()) -> MenuResponse:
    return await response.update_menu(menu_id, menu)


@router.delete("/menus/{menu_id}")
async def delete_menu(menu_id: int, response: MenuService = Depends()) -> dict:
    return await response.del_menu(menu_id)


@router.get("/menus/ORM/{menu_id}")
async def get_menu_orm(menu_id: int, response: MenuService = Depends()) -> MenuResponse:
    return await response.orm_read_menu(menu_id)
