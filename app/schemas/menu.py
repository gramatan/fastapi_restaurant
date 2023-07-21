from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    pass

class S_Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True
