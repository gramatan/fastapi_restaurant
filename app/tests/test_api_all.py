import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.main import app
from app.tests.conftest import URL

global_data = {
    'menu_id': None,
    'menu_title': None,
    'menu_description': None,
    'submenu_id': None,
    'submenu_title': None,
    'submenu_description': None,
    'dish1_id': None,
    'dish1_title': None,
    'dish1_description': None,
    'dish1_price': None,
    'dish2_id': None,
    'dish2_title': None,
    'dish2_description': None,
    'dish2_price': None,
}


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=URL) as client:
        yield client


@pytest.mark.asyncio
async def test_aa_empty_menus():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get('/api/v1/menus')
        assert response.status_code == 200
        data = response.json()
        assert data == []


@pytest.mark.asyncio
async def test_ab_empty_submenus():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get('/api/v1/menus/8675309/submenus')
        assert response.status_code == 200
        data = response.json()
        assert data == []


@pytest.mark.asyncio
async def test_ac_empty_dishes():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get('/api/v1/menus/8675309/submenus/32167/dishes')
        assert response.status_code == 200
        data = response.json()
        assert data == []


@pytest.mark.asyncio
async def test_ad_create_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.post('/api/v1/menus', json={'title': 'menu1', 'description': 'Empty'})
        assert response.status_code == 201
        data = response.json()
        global_data['menu_id'] = data['id']
        global_data['menu_title'] = data['title']
        global_data['menu_description'] = data['description']
        assert 'id' in data
        assert 'title' in data
        assert 'description' in data


@pytest.mark.asyncio
async def test_ae_create_submenu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.post(f'/api/v1/menus/{global_data["menu_id"]}/submenus',
                                     json={'title': 'sub1', 'description': 'empty'})
        assert response.status_code == 201
        data = response.json()
        global_data['submenu_id'] = data['id']
        global_data['submenu_title'] = data['title']
        global_data['submenu_description'] = data['description']
        assert 'id' in data
        assert 'title' in data
        assert 'description' in data


@pytest.mark.asyncio
async def test_af_create_dish1() -> None:
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.post(
            f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes',
            json={'title': 'dish1', 'description': 'Nope', 'price': '100.23'})
        assert response.status_code == 201
        data = response.json()
        global_data['dish1_id'] = data['id']
        global_data['dish1_title'] = data['title']
        global_data['dish1_description'] = data['description']
        global_data['dish1_price'] = data['price']
        assert 'id' in data
        assert 'title' in data
        assert 'description' in data
        assert 'price' in data


@pytest.mark.asyncio
async def test_ag_create_dish2() -> None:
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.post(
            f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes',
            json={'title': 'dish2', 'description': 'Nope again', 'price': '200.34'})
        assert response.status_code == 201
        data = response.json()
        global_data['dish2_id'] = data['id']
        assert 'id' in data
        assert 'title' in data
        assert 'description' in data
        assert 'price' in data


@pytest.mark.asyncio
async def test_ah_update_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.patch(f'/api/v1/menus/{global_data["menu_id"]}', json={'title': 'New_menu', 'description': 'New_d'})
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['menu_id']
        assert data['title'] == 'New_menu'
        assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_ai_update_submenu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.patch(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}',
                                      json={'title': 'New_submenu', 'description': 'New_d'})
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['submenu_id']
        assert data['title'] == 'New_submenu'
        assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_aj_update_dish():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.patch(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes/{global_data["dish1_id"]}',
                                      json={'title': 'New_dish', 'description': 'New_d', 'price': '100.23'})
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['dish1_id']
        assert data['title'] == 'New_dish'
        assert data['description'] == 'New_d'
        assert data['price'] == '100.23'


@pytest.mark.asyncio
async def test_ak_get_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['menu_id']
        assert data['title'] == 'New_menu'
        assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_al_get_list_menus():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get('/api/v1/menus')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]['id'] == global_data['menu_id']
        assert data[0]['title'] == 'New_menu'
        assert data[0]['description'] == 'New_d'


@pytest.mark.asyncio
async def test_am_get_list_submenus():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}/submenus')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]['id'] == global_data['submenu_id']
        assert data[0]['title'] == 'New_submenu'
        assert data[0]['description'] == 'New_d'


@pytest.mark.asyncio
async def test_an_get_list_dishes():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


@pytest.mark.asyncio
async def test_ao_get_submenu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['submenu_id']
        assert data['title'] == 'New_submenu'
        assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_ap_get_dish():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes/{global_data["dish1_id"]}')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['dish1_id']
        assert data['title'] == 'New_dish'
        assert data['description'] == 'New_d'
        assert data['price'] == '100.23'


@pytest.mark.asyncio
async def test_aq_delete_dish():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.delete(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}/dishes/{global_data["dish1_id"]}')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_ar_delete_submenu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.delete(f'/api/v1/menus/{global_data["menu_id"]}/submenus/{global_data["submenu_id"]}')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_as_get_submenu_list():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}/submenus')
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_at_get_menu_check_counts():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get(f'/api/v1/menus/{global_data["menu_id"]}')
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == global_data['menu_id']
        assert data['title'] == 'New_menu'
        assert data['description'] == 'New_d'
        assert data['submenus_count'] == 0
        assert data['dishes_count'] == 0


@pytest.mark.asyncio
async def test_au_delete_menu():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.delete(f'/api/v1/menus/{global_data["menu_id"]}')
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_av_get_menu_list():
    async with AsyncClient(app=app, base_url=URL) as client:
        global global_data
        response = await client.get('/api/v1/menus')
        assert response.status_code == 200
        assert response.json() == []
