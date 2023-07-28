from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuResponse(MenuBase):
    id: str | int
    submenus_count: int
    dishes_count: int

    class ConfigDict:
        from_attributes = True
