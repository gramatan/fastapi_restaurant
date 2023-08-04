from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Dish
from app.database.utils import get_db
from app.database.validator import validate_menu_submenu_dish
from app.schemas.dish import DishBase, DishResponse


class DishRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def read_dishes(self, submenu_id: int | str, menu_id: int | str):
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        result = await self.db.execute(select(Dish).where(Dish.submenu_id == submenu_id and Dish.submenu.menu_id == menu_id))
        dishes = result.scalars().all()
        dishes_list = []
        for dish in dishes:
            dish_dict = dish.__dict__
            dish_dict['id'] = str(dish_dict['id'])
            dish_dict['price'] = str(round(dish_dict['price'], 2))
            dishes_list.append(DishResponse(**dish_dict))
        return dishes_list

    async def create_dish(self, dish: DishBase, submenu_id: int | str, menu_id: int | str) -> DishResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        db_menu, db_submenu = await validate_menu_submenu_dish(self.db, menu_id, submenu_id)
        db_submenu.dishes_count += 1
        db_menu.dishes_count += 1
        await self.db.commit()

        db_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
        self.db.add(db_dish)
        await self.db.commit()
        await self.db.refresh(db_dish)

        dish_dict = db_dish.__dict__
        dish_dict['id'] = str(dish_dict['id'])
        dish_dict['price'] = str(round(dish_dict['price'], 2))

        return DishResponse(**dish_dict)

    async def read_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str) -> DishResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        dish_id = int(dish_id)
        db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(self.db, menu_id, submenu_id, int(dish_id))

        dish_dict = db_dish.__dict__
        dish_dict['id'] = str(dish_dict['id'])
        dish_dict['price'] = str(round(dish_dict['price'], 2))

        return DishResponse(**dish_dict)

    async def update_dish(self, dish_id: int | str, dish: DishBase,
                          submenu_id: int | str, menu_id: int | str) -> DishResponse:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        dish_id = int(dish_id)
        db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(self.db, menu_id, submenu_id, dish_id)

        for var, value in vars(dish).items():
            setattr(db_dish, var, value) if value else None
        await self.db.commit()
        await self.db.refresh(db_dish)

        dish_dict = db_dish.__dict__
        dish_dict['id'] = str(dish_dict['id'])
        dish_dict['price'] = str(round(dish_dict['price'], 2))

        return DishResponse(**dish_dict)

    async def del_dish(self, dish_id: int | str, submenu_id: int | str, menu_id: int | str) -> dict:
        menu_id = int(menu_id)
        submenu_id = int(submenu_id)
        dish_id = int(dish_id)
        db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(self.db, menu_id, submenu_id, dish_id)

        db_submenu.dishes_count -= 1
        db_menu.dishes_count -= 1
        await self.db.commit()

        await self.db.execute(delete(Dish).where(Dish.id == dish_id))
        await self.db.commit()
        return {'message': f'Dish {dish_id} deleted successfully.'}
