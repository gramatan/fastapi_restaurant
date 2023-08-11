from fastapi import APIRouter, BackgroundTasks, Depends

from app.schemas.submenu import SubMenuBase, SubMenuResponse
from app.services.submenu_service import SubmenuService

router = APIRouter()


@router.get('/submenus')
async def get_submenus(menu_id: int | str, response: SubmenuService = Depends(),
                       background_tasks: BackgroundTasks = BackgroundTasks()) -> list[SubMenuResponse]:
    return await response.read_submenus(menu_id)


@router.post('/submenus', status_code=201)
async def post_submenu(submenu: SubMenuBase, menu_id: int | str,
                       response: SubmenuService = Depends(SubmenuService),
                       background_tasks: BackgroundTasks = BackgroundTasks()) -> SubMenuResponse:
    return await response.create_submenu(submenu, menu_id)


@router.get('/submenus/{submenu_id}')
async def get_submenu(menu_id: int | str, submenu_id: int | str,
                      response: SubmenuService = Depends(),
                      background_tasks: BackgroundTasks = BackgroundTasks()) -> SubMenuResponse:
    return await response.read_submenu(submenu_id, menu_id)


@router.patch('/submenus/{submenu_id}')
async def patch_submenu(menu_id: int | str, submenu_id: int | str, submenu: SubMenuBase,
                        response: SubmenuService = Depends(),
                        background_tasks: BackgroundTasks = BackgroundTasks()) -> SubMenuResponse:
    return await response.update_submenu(submenu_id, submenu, menu_id)


@router.delete('/submenus/{submenu_id}')
async def delete_submenu(menu_id: int | str, submenu_id: int | str,
                         response: SubmenuService = Depends(),
                         background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    return await response.del_submenu(submenu_id, menu_id)
