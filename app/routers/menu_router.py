from fastapi import APIRouter, BackgroundTasks, Depends

from app.schemas.menu import MenuBase, MenuResponse
from app.services.menu_service import MenuService

router = APIRouter()


@router.get('/menus', response_model=list[MenuResponse])
async def get_menus(response: MenuService = Depends(),
                    background_tasks: BackgroundTasks = BackgroundTasks()):
    return await response.read_menus()


@router.post('/menus', status_code=201)
async def post_menu(menu: MenuBase, response: MenuService = Depends(),
                    background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuResponse:
    return await response.create_menu(menu)


@router.get('/menus/{menu_id}')
async def get_menu(menu_id: int | str, response: MenuService = Depends(),
                   background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuResponse:
    return await response.read_menu(menu_id)


@router.patch('/menus/{menu_id}')
async def patch_menu(menu_id: int | str, menu: MenuBase, response: MenuService = Depends(),
                     background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuResponse:
    return await response.update_menu(menu_id, menu)


@router.delete('/menus/{menu_id}')
async def delete_menu(menu_id: int | str, response: MenuService = Depends(),
                      background_tasks: BackgroundTasks = BackgroundTasks()) -> dict:
    return await response.del_menu(menu_id)


@router.get('/menus/ORM/{menu_id}')
async def get_menu_orm(menu_id: int | str, response: MenuService = Depends(),
                       background_tasks: BackgroundTasks = BackgroundTasks()) -> MenuResponse:
    return await response.orm_read_menu(menu_id)
