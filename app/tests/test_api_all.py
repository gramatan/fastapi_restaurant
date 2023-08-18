import pytest
from httpx import AsyncClient

from app.tests.conftest import reverse_url

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


@pytest.mark.asyncio
async def test_aa_empty_menus(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_menus'))
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_ab_empty_submenus(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_submenus', menu_id=8675309))
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_ac_empty_dishes(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_dishes', menu_id=8675309, submenu_id=32167))
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_ad_create_menu(client: AsyncClient):
    global global_data
    response = await client.post(reverse_url('post_menu'), json={'title': 'menu1', 'description': 'Empty'})
    assert response.status_code == 201
    data = response.json()
    global_data['menu_id'] = data['id']
    global_data['menu_title'] = data['title']
    global_data['menu_description'] = data['description']
    assert 'id' in data
    assert 'title' in data
    assert 'description' in data


@pytest.mark.asyncio
async def test_ae_create_submenu(client: AsyncClient):
    global global_data
    response = await client.post(reverse_url('post_submenu', menu_id=global_data['menu_id']),
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
async def test_af_create_dish1(client: AsyncClient) -> None:
    global global_data
    response = await client.post(
        reverse_url('post_dish', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id']),
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
async def test_ag_create_dish2(client: AsyncClient) -> None:
    global global_data
    response = await client.post(
        reverse_url('post_dish', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id']),
        json={'title': 'dish2', 'description': 'Nope again', 'price': '200.34'})
    assert response.status_code == 201
    data = response.json()
    global_data['dish2_id'] = data['id']
    assert 'id' in data
    assert 'title' in data
    assert 'description' in data
    assert 'price' in data


@pytest.mark.asyncio
async def test_ah_update_menu(client: AsyncClient):
    global global_data
    response = await client.patch(reverse_url('patch_menu', menu_id=global_data['menu_id']),
                                  json={'title': 'New_menu', 'description': 'New_d'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['menu_id']
    assert data['title'] == 'New_menu'
    assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_ai_update_submenu(client: AsyncClient):
    global global_data
    response = await client.patch(
        reverse_url('patch_submenu', menu_id=global_data['menu_id'],
                    submenu_id=global_data['submenu_id']),
        json={'title': 'New_submenu', 'description': 'New_d'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['submenu_id']
    assert data['title'] == 'New_submenu'
    assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_aj_update_dish(client: AsyncClient):
    global global_data
    response = await client.patch(
        reverse_url('patch_dish', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id'],
                    dish_id=global_data['dish1_id']),
        json={'title': 'New_dish', 'description': 'New_d', 'price': '100.23'})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['dish1_id']
    assert data['title'] == 'New_dish'
    assert data['description'] == 'New_d'
    assert data['price'] == '100.23'


@pytest.mark.asyncio
async def test_ak_get_menu(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_menu', menu_id=global_data['menu_id']))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['menu_id']
    assert data['title'] == 'New_menu'
    assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_al_get_list_menus(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_menus'))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['id'] == global_data['menu_id']
    assert data[0]['title'] == 'New_menu'
    assert data[0]['description'] == 'New_d'


@pytest.mark.asyncio
async def test_am_get_list_submenus(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_submenus', menu_id=global_data['menu_id']))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['id'] == global_data['submenu_id']
    assert data[0]['title'] == 'New_submenu'
    assert data[0]['description'] == 'New_d'


@pytest.mark.asyncio
async def test_an_get_list_dishes(client: AsyncClient):
    global global_data
    response = await client.get(
        reverse_url('get_dishes', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id']))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_ao_get_submenu(client: AsyncClient):
    global global_data
    response = await client.get(
        reverse_url('get_submenu', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id']))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['submenu_id']
    assert data['title'] == 'New_submenu'
    assert data['description'] == 'New_d'


@pytest.mark.asyncio
async def test_ap_get_dish(client: AsyncClient):
    global global_data
    response = await client.get(
        reverse_url('get_dish', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id'],
                    dish_id=global_data['dish1_id']))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['dish1_id']
    assert data['title'] == 'New_dish'
    assert data['description'] == 'New_d'
    assert data['price'] == '100.23'


@pytest.mark.asyncio
async def test_aq_delete_dish(client: AsyncClient):
    global global_data
    response = await client.delete(
        reverse_url('delete_dish', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id'],
                    dish_id=global_data['dish1_id']))
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ar_delete_submenu(client: AsyncClient):
    global global_data
    response = await client.delete(
        reverse_url('delete_submenu', menu_id=global_data['menu_id'], submenu_id=global_data['submenu_id']))
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_as_get_submenu_list(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_submenus', menu_id=global_data['menu_id']))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_at_get_menu_check_counts(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_menu', menu_id=global_data['menu_id']))
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == global_data['menu_id']
    assert data['title'] == 'New_menu'
    assert data['description'] == 'New_d'
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0


@pytest.mark.asyncio
async def test_au_delete_menu(client: AsyncClient):
    global global_data
    response = await client.delete(reverse_url('delete_menu', menu_id=global_data['menu_id']))
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_av_get_menu_list(client: AsyncClient):
    global global_data
    response = await client.get(reverse_url('get_menus'))
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_aw_get_all(client: AsyncClient):
    response = await client.post(reverse_url('post_menu'), json={'title': 'Menu 1', 'description': 'Description 1'})
    assert response.status_code == 201
    menu1_data = response.json()

    response = await client.post(reverse_url('post_menu'), json={'title': 'Menu 2', 'description': 'Description 2'})
    assert response.status_code == 201
    menu2_data = response.json()

    response = await client.post(reverse_url('post_submenu', menu_id=menu2_data['id']),
                                 json={'title': 'SubMenu 2.1', 'description': 'SubMenu Description 2.1'})
    assert response.status_code == 201

    response = await client.post(reverse_url('post_menu'), json={'title': 'Menu 3', 'description': 'Description 3'})
    assert response.status_code == 201
    menu3_data = response.json()

    response = await client.post(reverse_url('post_submenu', menu_id=menu3_data['id']),
                                 json={'title': 'SubMenu 3.1', 'description': 'SubMenu Description 3.1'})
    assert response.status_code == 201
    submenu3_1_data = response.json()

    response = await client.post(reverse_url('post_dish', menu_id=menu3_data['id'], submenu_id=submenu3_1_data['id']),
                                 json={'title': 'Dish 3.1.1', 'description': 'Dish Description 3.1.1', 'price': '100.23'})
    assert response.status_code == 201

    response = await client.post(reverse_url('post_dish', menu_id=menu3_data['id'], submenu_id=submenu3_1_data['id']),
                                 json={'title': 'Dish 3.1.2', 'description': 'Dish Description 3.1.2', 'price': '110.23'})
    assert response.status_code == 201

    response = await client.post(reverse_url('post_submenu', menu_id=menu3_data['id']),
                                 json={'title': 'SubMenu 3.2', 'description': 'SubMenu Description 3.2'})
    assert response.status_code == 201
    submenu3_2_data = response.json()

    response = await client.get(reverse_url('all'))
    assert response.status_code == 200
    full_data = response.json()
    assert isinstance(full_data, dict)
    assert 'menus' in full_data

    assert len(full_data['menus']) >= 3

    for menu in full_data['menus']:
        if menu['id'] == menu1_data['id']:
            assert menu['title'] == 'Menu 1'
            assert menu['description'] == 'Description 1'
            assert 'submenus' not in menu

        elif menu['id'] == menu2_data['id']:
            assert menu['title'] == 'Menu 2'
            assert menu['description'] == 'Description 2'
            assert len(menu['submenus']) == 1

        elif menu['id'] == menu3_data['id']:
            assert menu['title'] == 'Menu 3'
            assert menu['description'] == 'Description 3'
            assert len(menu['submenus']) == 2

            for submenu in menu['submenus']:
                if submenu['id'] == submenu3_1_data['id']:
                    assert submenu['title'] == 'SubMenu 3.1'
                    assert submenu['description'] == 'SubMenu Description 3.1'
                    assert len(submenu['dishes']) == 2

                elif submenu['id'] == submenu3_2_data['id']:
                    assert submenu['title'] == 'SubMenu 3.2'
                    assert submenu['description'] == 'SubMenu Description 3.2'
                    assert 'dishes' not in submenu

    await client.delete(reverse_url('delete_menu', menu_id=menu1_data['id']))

    await client.delete(reverse_url('delete_menu', menu_id=menu2_data['id']))

    await client.delete(reverse_url('delete_menu', menu_id=menu3_data['id']))

    response = await client.get(reverse_url('all'))
    assert response.status_code == 200
    full_data = response.json()
    assert isinstance(full_data, dict)
    assert 'menus' in full_data

    assert len(full_data['menus']) == 0
