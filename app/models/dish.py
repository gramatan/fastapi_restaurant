from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)
    submenu_id = Column(Integer, index=True)
