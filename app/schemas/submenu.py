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

    class Config:
        from_attributes = True
