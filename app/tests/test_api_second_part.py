import pytest
from httpx import AsyncClient

# IMPORTANT: For these tests we need an empty database because of empty lists of menus expected
# URL = "http://127.0.0.1:8000"   # local
URL = "http://127.0.0.1:8001"   # Docker

@pytest.mark.asyncio
async def test_get_empty_list() -> None:
    # empty list of menus
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    data = response.json()
    assert data == []
    # empty list of submenus
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get("/api/v1/menus/9999/submenus")
    assert response.status_code == 200
    data = response.json()
    assert data == []
    # empty list of dishes
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get("/api/v1/menus/9999/submenus/9999/dishes")
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_create_menu_submenu_dish_get_lists_update_data() -> None:
    # create menu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post("/api/v1/menus", json={"title": "menu1", "description": "Empty"})
        menu_id = response.json()["id"]

    # create submenu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={"title": "sub1", "description": "empty"})
        sub_data = response.json()
    submenu_id = sub_data["id"]

    # create dish
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                                 json={"title": "dish1", "description": "Nope", "price": "100"})
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                                 json={"title": "dish2", "description": "Nope again", "price": "200"})

    # get menu lists
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "title" in data[0]
    assert data[0]["title"] == "menu1"
    assert "description" in data[0]
    assert data[0]["description"] == "Empty"
    assert "id" in data[0]
    assert data[0]["id"] == menu_id

    # get submenu lists
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "title" in data[0]
    assert data[0]["title"] == "sub1"
    assert "description" in data[0]
    assert data[0]["description"] == "empty"
    assert "id" in data[0]
    assert data[0]["id"] == submenu_id

    # get dish lists
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # update menu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.patch(f"/api/v1/menus/{menu_id}", json={"title": "menu1_updated", "description": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "menu1_updated"
    assert data["description"] == "Updated"
    assert "id" in data
    assert data["id"] == menu_id

    # update submenu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}",
                                json={"title": "sub1_updated", "description": "updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "sub1_updated"
    assert data["description"] == "updated"
    assert "id" in data
    assert data["id"] == submenu_id

    # update dish
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/1",
                                json={"title": "dish1_updated", "description": "updated", "price": "300"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "dish1_updated"
    assert data["description"] == "updated"
    assert data["price"] == "300.00"
    assert "id" in data

    # delete dish
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/2")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Dish 2 deleted successfully."

    # delete submenu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Submenu {submenu_id} deleted successfully."

    # delete menu
    async with AsyncClient(base_url=URL) as ac:
        response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Menu {menu_id} deleted successfully."

