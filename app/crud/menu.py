from sqlalchemy.orm import Session
from app.models.menu import Menu
from app.schemas.menu import MenuCreate


def get_menu(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()


def create_menu(db: Session, menu: MenuCreate):
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu
