import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.crud import menu as crud_menu, submenu as crud_submenu
from app.schemas import MenuBase, SubMenuBase
from app.database.base import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_create_and_read_submenu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id

        assert db_submenu.title == submenu_in.title
        assert db_submenu.description == submenu_in.description

        # Read submenu
        submenu_from_db = await crud_submenu.read_submenu(session, submenu_id, menu_id)

        assert submenu_from_db.title == submenu_in.title
        assert submenu_from_db.description == submenu_in.description

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_update_submenu(db_session: AsyncSession) -> None:
    # Create menu
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id

        # Update submenu
        submenu_update = SubMenuBase(title="Updated SubMenu", description="This is an updated test submenu")
        updated_submenu = await crud_submenu.update_submenu(session, submenu_id, submenu_update, menu_id)

        assert updated_submenu.title == submenu_update.title
        assert updated_submenu.description == submenu_update.description

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_delete_submenu(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id


        # Delete submenu
        delete_response = await crud_submenu.del_submenu(session, submenu_id, menu_id)

        assert delete_response == {"message": f"Submenu {submenu_id} deleted successfully."}

        with pytest.raises(HTTPException):
            await crud_submenu.read_submenu(session, submenu_id, menu_id)

        # cleanup
        await crud_menu.del_menu(session, menu_id)
