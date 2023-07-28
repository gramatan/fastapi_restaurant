import pytest

from fastapi import HTTPException

from app.database import SubMenu, Menu
from app.schemas import SubMenuBase, MenuBase
from app.crud import dish as crud_dish
from app.schemas import DishBase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.database.base import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_create_and_read_dish(db_session: AsyncSession) -> None:
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
        sub_id = db_submenu.id

    async for session in db_session:
        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price=10.0)
        dish = await crud_dish.create_dish(session, dish_in, id, sub_id)
        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Read the dish back from the database
        dish_from_db = await crud_dish.read_dish(session, dish_in, id, sub_id)
        assert dish_from_db.title == dish_in.title
        assert dish_from_db.description == dish_in.description
        assert dish_from_db.price == dish_in.price


@pytest.mark.asyncio
async def test_update_dish(db_session: AsyncSession) -> None:
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
        sub_id = db_submenu.id

    async for session in db_session:
        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price=10.0)
        dish = await crud_dish.create_dish(session, dish_in, id, sub_id)
        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Update the dish
        dish_update = DishBase(title="Updated Dish", description="not a yoghurt", price=20.0)
        updated_dish = await crud_dish.update_dish(session, dish.id, dish_update, id, sub_id)

        assert updated_dish.title == dish_update.title
        assert updated_dish.description == dish_update.description
        assert updated_dish.price == dish_update.price


@pytest.mark.asyncio
async def test_delete_dish(db_session: AsyncSession) -> None:
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
        sub_id = db_submenu.id

    async for session in db_session:
        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price=10.0)
        dish = await crud_dish.create_dish(session, dish_in, id, sub_id)
        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Delete the dish
        delete_response = await crud_dish.del_dish(session, dish.id, id, sub_id)

        # Check if the deletion was successful
        assert delete_response == {"message": f"Dish {dish.id} deleted successfully."}

        # Expect an HTTPException
        with pytest.raises(HTTPException):
            await crud_dish.read_dish(session, dish.id, id, sub_id)
