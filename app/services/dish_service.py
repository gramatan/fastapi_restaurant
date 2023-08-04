from fastapi import Depends

from app.repository.dish import DishRepository


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends()):
        self.dish_repository = dish_repository

    def read_dishes(self, submenu_id: int | str, menu_id: int | str):
        return self.dish_repository.read_dishes(submenu_id, menu_id)

    def create_dish(self, dish_data, submenu_id: int | str, menu_id: int | str):
        return self.dish_repository.create_dish(dish_data, submenu_id, menu_id)

    def read_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        return self.dish_repository.read_dish(dish_id, submenu_id, menu_id)

    def update_dish(self, dish_id: int | str, dish_data, submenu_id: int | str, menu_id: int | str):
        return self.dish_repository.update_dish(dish_id, dish_data, submenu_id, menu_id)

    def del_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str):
        return self.dish_repository.del_dish(dish_id, submenu_id, menu_id)
