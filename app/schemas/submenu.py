from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    pass


class SchemasSubMenu(SubMenuBase):
    id: str | int
    dish_count: int = 0

    class Config:
        from_attributes = True
