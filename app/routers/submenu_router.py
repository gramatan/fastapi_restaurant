from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.submenu import read_submenus, create_submenu, read_submenu, update_submenu, del_submenu
from app.database.utils import get_db
from app.schemas.submenu import SubMenuResponse, SubMenuBase

router = APIRouter()


@router.get("/")
async def get_submenus(menu_id: int, db: AsyncSession = Depends(get_db)) -> List[SubMenuResponse]:
    return await read_submenus(db, menu_id)


@router.post("/", status_code=201)
async def post_submenu(submenu: SubMenuBase, menu_id: int, db: AsyncSession = Depends(get_db)) -> SubMenuResponse:
    return await create_submenu(db, submenu, menu_id)


@router.get("/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)) -> SubMenuResponse:
    return await read_submenu(db, submenu_id, menu_id)


@router.patch("/{submenu_id}")
async def patch_submenu(menu_id: int, submenu_id: int, submenu: SubMenuBase, db: AsyncSession = Depends(get_db)) -> SubMenuResponse:
    return await update_submenu(db, submenu_id, submenu, menu_id)


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    return await del_submenu(db, submenu_id, menu_id)
