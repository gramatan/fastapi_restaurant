from asyncio import current_task
from contextlib import asynccontextmanager

from decouple import config
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL_DOCKER')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()   # type: ignore


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        async_session,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


class Menu(Base):  # type: ignore
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    manual_id = Column(String, unique=True, nullable=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    submenus = relationship('SubMenu', backref='menu', cascade='all, delete-orphan')


class SubMenu(Base):  # type: ignore
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True, index=True)
    manual_id = Column(String, unique=True, nullable=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))

    dishes = relationship('Dish', backref='submenu', cascade='all, delete-orphan')


class Dish(Base):  # type: ignore
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    manual_id = Column(String, unique=True, nullable=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Numeric(precision=10, scale=2), index=True)
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))
