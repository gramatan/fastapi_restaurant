from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.crud.validator import validate_menu_submenu_dish
from app.database import Dish
from app.schemas import DishBase, DishResponse


async def read_dishes(db: Session, submenu_id: int, menu_id: int):
    menu_id = int(menu_id)
    submenu_id = int(submenu_id)
    result = await db.execute(select(Dish).where(Dish.submenu_id == submenu_id and Dish.submenu.menu_id == menu_id))
    dishes = result.scalars().all()
    dishes_list = []
    for dish in dishes:
        dish_dict = dish.__dict__
        dish_dict["id"] = str(dish_dict["id"])
        dish_dict["price"] = str(round(dish_dict["price"], 2))
        dishes_list.append(DishResponse(**dish_dict))
    return dishes_list


async def create_dish(db: Session, dish: DishBase, submenu_id: int, menu_id: int) -> DishResponse:
    menu_id = int(menu_id)
    submenu_id = int(submenu_id)
    db_menu, db_submenu = await validate_menu_submenu_dish(db, menu_id, submenu_id)
    db_submenu.dishes_count += 1
    db_menu.dishes_count += 1
    await db.commit()

    db_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
    db.add(db_dish)
    await db.commit()
    await db.refresh(db_dish)

    dish_dict = db_dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))

    return DishResponse(**dish_dict)


async def read_dish(db: Session, dish_id: int, submenu_id: int, menu_id: int) -> DishResponse:
    menu_id = int(menu_id)
    submenu_id = int(submenu_id)
    dish_id = int(dish_id)
    db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(db, menu_id, submenu_id, int(dish_id))

    dish_dict = db_dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))

    return DishResponse(**dish_dict)


async def update_dish(db: Session, dish_id: int, dish: DishBase, submenu_id: int, menu_id: int) -> DishResponse:
    menu_id = int(menu_id)
    submenu_id = int(submenu_id)
    dish_id = int(dish_id)
    db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(db, menu_id, submenu_id, dish_id)

    for var, value in vars(dish).items():
        setattr(db_dish, var, value) if value else None
    await db.commit()
    await db.refresh(db_dish)

    dish_dict = db_dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))

    return DishResponse(**dish_dict)


async def del_dish(db: Session, dish_id: int, submenu_id: int, menu_id: int) -> dict:
    menu_id = int(menu_id)
    submenu_id = int(submenu_id)
    dish_id = int(dish_id)
    db_menu, db_submenu, db_dish = await validate_menu_submenu_dish(db, menu_id, submenu_id, dish_id)

    db_submenu.dishes_count -= 1
    db_menu.dishes_count -= 1
    await db.commit()

    await db.execute(delete(Dish).where(Dish.id == dish_id))
    await db.commit()
    return {"message": f"Dish {dish_id} deleted successfully."}
