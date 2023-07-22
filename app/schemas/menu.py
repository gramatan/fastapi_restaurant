from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuResponse(MenuBase):
    id: str | int
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        from_attributes = True
