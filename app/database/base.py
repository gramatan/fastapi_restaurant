import logging
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@db/resto"
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@localhost/resto"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    submenus = relationship('SubMenu', backref='menu', cascade='all, delete-orphan')


class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))
    dishes_count = Column(Integer, default=0)

    dishes = relationship('Dish', backref='submenu', cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Numeric(precision=10, scale=2), index=True)
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'))


async def create_tables():
    logging.info("Creating tables")
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@localhost/resto"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Tables created")


async def drop_tables():
    logging.info("Dropping tables")
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ylab:no_secure_password@localhost/resto"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logging.info("Tables dropped")
