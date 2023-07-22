from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database import Dish, SubMenu
from app.schemas import DishBase, DishResponse


def read_dishes(db: Session):
    dishes = db.query(Dish).all()
    dishes_list = []
    for dish in dishes:
        dish_dict = dish.__dict__
        dish_dict["id"] = str(dish_dict["id"])
        dish_dict["price"] = str(round(dish_dict["price"], 2))
        dishes_list.append(DishResponse(**dish_dict))
    return dishes_list


def create_dish(db: Session, dish: DishBase, submenu_id: int) -> DishResponse:
    db_submenu = db.query(SubMenu).get(submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    db_submenu.dishes_count += 1
    db_submenu.menu.dishes_count += 1
    db.commit()

    db_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    dish_dict = db_dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))

    return DishResponse(**dish_dict)


def read_dish(db: Session, dish_id: int) -> DishResponse:
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_dict = dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))
    return DishResponse(**dish_dict)


def update_dish(db: Session, dish_id: int, dish: DishBase) -> DishResponse:
    db_dish = db.get(Dish, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    for var, value in vars(dish).items():
        setattr(db_dish, var, value) if value else None
    db.commit()
    db.refresh(db_dish)

    dish_dict = db_dish.__dict__
    dish_dict["id"] = str(dish_dict["id"])
    dish_dict["price"] = str(round(dish_dict["price"], 2))

    return DishResponse(**dish_dict)


def del_dish(db: Session, dish_id: int) -> dict:
    db_dish = db.get(Dish, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")

    db_submenu = db.query(SubMenu).get(db_dish.submenu_id)
    db_submenu.dishes_count -= 1
    db_submenu.menu.dishes_count -= 1
    db.commit()

    db.execute(delete(Dish).where(Dish.id == dish_id))
    db.commit()
    return {"message": f"Dish {dish_id} deleted successfully."}
