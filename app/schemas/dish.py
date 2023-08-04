from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishResponse(DishBase):
    id: int | str

    class ConfigDict:
        from_attributes = True
