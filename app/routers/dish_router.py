from typing import List

from fastapi import APIRouter, Depends

from app.schemas.dish import DishResponse, DishBase
from app.services.dish_service import DishService

router = APIRouter()


@router.get("/dishes")
async def get_dishes(menu_id: int, submenu_id: int, response: DishService = Depends()) -> List[DishResponse]:
    return await response.read_dishes(submenu_id, menu_id)


@router.post("/dishes", status_code=201)
async def post_dish(menu_id: int, submenu_id: int, dish: DishBase, response: DishService = Depends()) -> DishResponse:
    return await response.create_dish(dish, submenu_id, menu_id)


@router.get("/dishes/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int | str, response: DishService = Depends()) -> DishResponse:
    return await response.read_dish(dish_id, submenu_id, menu_id)


@router.patch("/dishes/{dish_id}")
async def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishBase, response: DishService = Depends()) -> DishResponse:
    return await response.update_dish(dish_id, dish, submenu_id, menu_id)


@router.delete("/dishes/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int, response: DishService = Depends()) -> dict:
    return await response.del_dish(dish_id, submenu_id, menu_id)
