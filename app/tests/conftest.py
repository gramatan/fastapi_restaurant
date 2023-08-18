import asyncio

import pytest_asyncio
from decouple import config
from httpx import AsyncClient

from app.main import app

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL_DOCKER')
URL = 'http://web:8000'


def reverse_url(route_name: str, **kwargs) -> str:
    routes = {
        'all': '/api/v1/all',
        'get_menus': '/api/v1/menus',
        'post_menu': '/api/v1/menus',
        'get_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'patch_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'delete_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'get_menu_orm': f'/api/v1/menus/ORM/{kwargs.get("menu_id", "")}',
        'get_submenus': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'post_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'get_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'patch_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'delete_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'get_dishes': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'post_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'get_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                    f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'patch_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                      f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'delete_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                       f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
    }

    return str(routes.get(route_name))


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(app=app, base_url=URL) as client:
        yield client
        await client.aclose()
