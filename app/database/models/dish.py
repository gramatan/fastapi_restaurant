from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from app.database.base import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Numeric(precision=10, scale=2), index=True)
    submenu_id = Column(Integer, ForeignKey('submenus.id'))
