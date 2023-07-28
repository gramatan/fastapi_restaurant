from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuResponse(SubMenuBase):
    id: str | int
    dishes_count: int

    class ConfigDict:
        from_attributes = True
