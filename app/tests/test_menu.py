import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.crud import menu as crud_menu
from app.schemas.menu import MenuBase

from app.tests.conftest import SQLALCHEMY_DATABASE_URL


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
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        assert menu.title == menu_in.title
        assert menu.description == menu_in.description

        # Read
        menu_from_db = await crud_menu.read_menu(session, menu_id)

        assert menu_from_db.title == menu_in.title
        assert menu_from_db.description == menu_in.description

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_update_menu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create
        menu_in = MenuBase(title="Test menu", description="Test menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Update
        menu_update = MenuBase(title="New name", description="New description")
        updated_menu = await crud_menu.update_menu(session, menu_id, menu_update)

        assert updated_menu.title == menu_update.title
        assert updated_menu.description == menu_update.description

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_delete_menu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create
        menu_in = MenuBase(title="Test menu", description="Test menu description")

        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Delete
        delete_response = await crud_menu.del_menu(session, menu_id)
        assert delete_response == {"message": f"Menu {menu_id} deleted successfully."}

        # Expect an HTTPException
        with pytest.raises(HTTPException):
            await crud_menu.read_menu(session, menu_id)
