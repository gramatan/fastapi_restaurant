import pytest
from fastapi import HTTPException
from app.database import Menu, SubMenu
from app.crud import menu as crud_menu, submenu as crud_submenu
from app.schemas import MenuBase, SubMenuBase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database.base import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_create_and_read_submenu(db_session: AsyncSession) -> None:
    # Create menu
    async for session in db_session:
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        db_menu = Menu(**menu_in.model_dump())
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        id = db_menu.id

    # Create submenu
    async for session in db_session:
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = SubMenu(menu_id=id, **submenu_in.model_dump())
        session.add(db_submenu)
        await session.commit()
        await session.refresh(db_submenu)

        assert db_submenu.title == submenu_in.title
        assert db_submenu.description == submenu_in.description

        # Read submenu
        submenu_from_db = await crud_submenu.read_submenu(session, db_submenu.id, db_menu.id)

        assert submenu_from_db.title == submenu_in.title
        assert submenu_from_db.description == submenu_in.description

@pytest.mark.asyncio
async def test_update_submenu(db_session: AsyncSession) -> None:
    # Create menu
    async for session in db_session:
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        db_menu = Menu(**menu_in.model_dump())
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        id = db_menu.id
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        await crud_menu.create_menu(session, menu_in)

    # Create submenu
    async for session in db_session:
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        submenu = await crud_submenu.create_submenu(session, submenu_in, id)

        # Update submenu
        submenu_update = SubMenuBase(title="Updated SubMenu", description="This is an updated test submenu")
        updated_submenu = await crud_submenu.update_submenu(session, submenu.id, submenu_update, id)

        assert updated_submenu.title == submenu_update.title
        assert updated_submenu.description == submenu_update.description

@pytest.mark.asyncio
async def test_delete_submenu(db_session: AsyncSession) -> None:
    # Create menu
    async for session in db_session:
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        db_menu = Menu(**menu_in.model_dump())
        session.add(db_menu)
        await session.commit()
        await session.refresh(db_menu)
        id = db_menu.id

    # Create submenu
    async for session in db_session:
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        submenu = await crud_submenu.create_submenu(session, submenu_in, id)

        # Delete submenu
        delete_response = await crud_submenu.del_submenu(session, submenu.id, id)

        assert delete_response == {"message": f"SubMenu {submenu.id} deleted successfully."}

        with pytest.raises(HTTPException):
            await crud_submenu.read_submenu(session, submenu.id, id)
