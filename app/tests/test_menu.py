import pytest
from fastapi import HTTPException

from app.database import Menu
from app.crud import menu as crud_menu
from app.schemas import MenuBase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database.base import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session

@pytest.mark.asyncio
async def test_create_and_read_menu(db_session: AsyncSession) -> None:

    async for session in db_session:
        # Create
        menu_in = MenuBase(title="Test menu", description="Test menu description")

        db_menu = Menu(**menu_in.model_dump())
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)

        assert db_menu.title == menu_in.title
        assert db_menu.description == menu_in.description

        # Read
        menu_from_db = await crud_menu.read_menu(session, db_menu.id)

        assert menu_from_db.title == menu_in.title
        assert menu_from_db.description == menu_in.description


@pytest.mark.asyncio
async def test_update_menu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create
        menu_in = MenuBase(title="Test menu", description="Test menu description")
        menu = await crud_menu.create_menu(session, menu_in)

        # Update
        menu_update = MenuBase(title="New name", description="New description")
        updated_menu = await crud_menu.update_menu(session, menu.id, menu_update)

        assert updated_menu.title == menu_update.title
        assert updated_menu.description == menu_update.description


@pytest.mark.asyncio
async def test_delete_menu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create
        menu_in = MenuBase(title="Test menu", description="Test menu description")

        menu = await crud_menu.create_menu(session, menu_in)

        # Delete
        delete_response = await crud_menu.del_menu(session, menu.id)

        # Deletion was successful
        assert delete_response == {"message": f"Menu {menu.id} deleted successfully."}

        # Expect an HTTPException
        with pytest.raises(HTTPException):
            await crud_menu.read_menu(session, menu.id)
