from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.database.base import Dish
from app.schemas.dish import DishBase, DishResponse
import logging
logging.basicConfig(level=logging.INFO)

def read_dishes(db: Session) -> list:
    return db.query(Dish).all()

def create_dish(db: Session, dish: DishBase, submenu_id: int) -> DishResponse:
    logging.info(dish)
    db_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    db_dish_dict = db_dish.__dict__
    db_dish_dict["id"] = str(db_dish_dict["id"])
    db_dish_dict["price"] = str(round(db_dish_dict["price"], 2))

    return DishResponse(**db_dish_dict)

def read_dish(db: Session, dish_id: int) -> DishResponse:
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_dict = {c.name: getattr(dish, c.name) for c in dish.__table__.columns}
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

    db_dish_dict = {c.name: getattr(db_dish, c.name) for c in db_dish.__table__.columns}
    db_dish_dict["id"] = str(db_dish_dict["id"])
    db_dish_dict["price"] = str(round(db_dish_dict["price"], 2))

    return DishResponse(**db_dish_dict)


def del_dish(db: Session, dish_id: int) -> dict:
    db_dish = db.get(Dish, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    db.execute(delete(Dish).where(Dish.id == dish_id))
    db.commit()
    return {"message": f"Dish {dish_id} deleted successfully."}
