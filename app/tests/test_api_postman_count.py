import pytest
from httpx import AsyncClient
from .conftest import URL


@pytest.mark.asyncio
async def test_number_of_dishes_and_submenus_in_menu() -> None:
    # Создает Меню
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post("/api/v1/menus", json={"title": "menu1", "description": "Empty"})
        menu_data = response.json()

    assert response.status_code == 201
    assert "id" in menu_data

    menu_id = menu_data["id"]

    # Создает подменю
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={"title": "sub1", "description": "empty"})
        sub_data = response.json()

    assert response.status_code == 201
    assert "id" in sub_data

    submenu_id = sub_data["id"]

    # Создает блюдо 1
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                                 json={"title": "dish1", "description": "Nope", "price": "100.23"})
    assert response.status_code == 201
    assert "id" in sub_data

    # Создает блюдо 2
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                                 json={"title": "dish2", "description": "Nope again", "price": "200.34"})
    assert response.status_code == 201
    assert "id" in sub_data

    # Просматривает определенное меню
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}")
    get_menu_data = response.json()

    assert response.status_code == 200
    assert "id" in get_menu_data
    assert get_menu_data["id"] == menu_id
    assert "submenus_count" in get_menu_data
    assert get_menu_data["submenus_count"] == 1
    assert "dishes_count" in get_menu_data
    assert get_menu_data["dishes_count"] == 2

    # Просматривает определенное подменю
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    get_submenu_data = response.json()

    assert response.status_code == 200
    assert "id" in get_submenu_data
    assert get_submenu_data["id"] == submenu_id
    assert "dishes_count" in get_submenu_data
    assert get_menu_data["dishes_count"] == 2

    # Удаляет подменю
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    get_submenu_data = response.json()

    assert response.status_code == 200
    assert get_submenu_data["message"] == f"Submenu {submenu_id} deleted successfully."

    # Просматривает список подменю
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")

    assert response.status_code == 200
    data = response.json()
    assert data == []

    # Просматривает список блюд
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == 200
    data = response.json()
    assert data == []

    # Просматривает определенное меню
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}")
    get_menu_data = response.json()

    assert response.status_code == 200
    assert get_menu_data["id"] == menu_id
    assert get_menu_data["submenus_count"] == 0
    assert get_menu_data["dishes_count"] == 0

    # Удаляет меню
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.delete(f"/api/v1/menus/{menu_id}")
    get_menu_data = response.json()

    assert response.status_code == 200
    assert get_menu_data["message"] == f"Menu {menu_id} deleted successfully."

    # Просматривает список меню
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    data = response.json()
    assert data == []

