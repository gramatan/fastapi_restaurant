from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.database import SubMenu, Menu
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
    db_menu = await db.get(Menu, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    db_menu.submenus_count += 1
    await db.commit()

    db_submenu = SubMenu(menu_id=menu_id, **submenu.model_dump())
    db.add(db_submenu)
    await db.commit()
    await db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])

    return SubMenuResponse(**submenu_dict)


async def read_submenu(db: Session, submenu_id: int) -> SubMenuResponse:
    submenu = await db.get(SubMenu, submenu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_dict = submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


async def update_submenu(db: Session, submenu_id: int, submenu: SubMenuBase) -> SubMenuResponse:
    db_submenu = await db.get(SubMenu, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    for var, value in vars(submenu).items():
        setattr(db_submenu, var, value) if value else None
    await db.commit()
    await db.refresh(db_submenu)
    submenu_dict = db_submenu.__dict__
    submenu_dict["id"] = str(submenu_dict["id"])
    return SubMenuResponse(**submenu_dict)


async def del_submenu(db: Session, submenu_id: int) -> dict:
    submenu = await db.get(SubMenu, submenu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    db_menu = await db.get(Menu, submenu.menu_id)
    db_menu.submenus_count -= 1
    db_menu.dishes_count -= submenu.dishes_count
    await db.commit()

    await db.execute(delete(SubMenu).where(SubMenu.id == submenu_id))
    await db.commit()
    return {"message": f"Submenu {submenu_id} deleted successfully."}
