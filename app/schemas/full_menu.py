from pydantic import BaseModel

from app.schemas.dish import DishBase
from app.schemas.menu import MenuBase
from app.schemas.submenu import SubMenuBase


class FullDishResponse(DishBase):
    id: int | str


class FullSubMenuResponse(SubMenuBase):
    id: int | str
    dishes: list[FullDishResponse]


class FullMenuResponse(MenuBase):
    id: int | str
    submenus: list[FullSubMenuResponse]


class FullMenuListResponse(BaseModel):
    menus: list[FullMenuResponse]
