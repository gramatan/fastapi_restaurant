import logging

from sqlalchemy.ext.asyncio import create_async_engine

from app.database.base import async_session, Base


async def get_db():
    async with async_session() as db:
        yield db


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