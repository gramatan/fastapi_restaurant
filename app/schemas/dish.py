from pydantic import BaseModel, Field


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class SchemasDish(DishBase):
    id: str | int

    class Config:
        from_attributes = True
