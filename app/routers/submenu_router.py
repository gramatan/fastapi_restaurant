from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.submenu import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
from app.database.utils import get_db
from app.schemas.submenu import SubMenuResponse, SubMenuBase
from app.services.submenu_service import SubmenuService

router = APIRouter()


@router.get("/submenus")
async def get_submenus(menu_id: int, response: SubmenuService = Depends()) -> List[SubMenuResponse]:
    return await response.read_submenus(menu_id)


@router.post("/submenus", status_code=201)
async def post_submenu(submenu: SubMenuBase, menu_id: int, response: SubmenuService = Depends()) -> SubMenuResponse:
    return await response.create_submenu(submenu, menu_id)


@router.get("/submenus/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int, response: SubmenuService = Depends()) -> SubMenuResponse:
    return await response.read_submenu(submenu_id, menu_id)


@router.patch("/submenus/{submenu_id}")
async def patch_submenu(menu_id: int, submenu_id: int, submenu: SubMenuBase, response: SubmenuService = Depends()) -> SubMenuResponse:
    return await response.update_submenu(submenu_id, submenu, menu_id)


@router.delete("/submenus/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int, response: SubmenuService = Depends()) -> dict:
    return await response.del_submenu(submenu_id, menu_id)
