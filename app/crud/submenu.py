from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.crud.validator import validate_menu_submenu_dish
from app.database import SubMenu
from app.schemas import SubMenuResponse, SubMenuBase


async def read_submenus(db: Session, menu_id: int) -> list[SubMenuResponse]:
    result = await db.execute(select(SubMenu).where(SubMenu.menu_id == menu_id))
    submenus = result.scalars().all()
    submenus_list = []
    for submenu in submenus:
        submenu_response = SubMenuResponse(**submenu.__dict__)
        submenu_response.id = str(submenu_response.id)
        submenus_list.append(submenu_response)
    return submenus_list


async def create_submenu(db: Session, submenu: SubMenuBase, menu_id: int) -> SubMenuResponse:
    db_menu = await validate_menu_submenu_dish(db, menu_id=menu_id)
    db_menu.submenus_count += 1
    await db.commit()

    db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
    db.add(db_submenu)
    await db.commit()
    await db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])

    return SubMenuResponse(**submenu_dict)


async def read_submenu(db: Session, submenu_id: int, menu_id: int) -> SubMenuResponse:
    db_menu, db_submenu = await validate_menu_submenu_dish(db, menu_id=menu_id, submenu_id=submenu_id)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


async def update_submenu(db: Session, submenu_id: int, submenu: SubMenuBase, menu_id: int) -> SubMenuResponse:
    db_menu, db_submenu = await validate_menu_submenu_dish(db, menu_id=menu_id, submenu_id=submenu_id)
    for var, value in vars(submenu).items():
        setattr(db_submenu, var, value) if value else None
    await db.commit()
    await db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


async def del_submenu(db: Session, submenu_id: int, menu_id: int) -> dict:
    db_menu, db_submenu = await validate_menu_submenu_dish(db, menu_id=menu_id, submenu_id=submenu_id)
    db_menu.submenus_count -= 1
    db_menu.dishes_count -= db_submenu.dishes_count
    await db.commit()

    await db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
    await db.commit()
    return {"message": f"Submenu {submenu_id} deleted successfully."}
