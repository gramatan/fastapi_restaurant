from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishResponse(DishBase):
    id: str | int

    class Config:
        from_attributes = True
