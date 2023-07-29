import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.crud import dish as crud_dish
from app.crud import submenu as crud_submenu
from app.crud import menu as crud_menu
from app.schemas.menu import MenuBase
from app.schemas.submenu import SubMenuBase
from app.schemas.dish import DishBase

from app.tests.conftest import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_create_and_read_dish(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id

        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price='10.00')
        dish = await crud_dish.create_dish(session, dish_in, submenu_id, menu_id)
        dish_id = dish.id

        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Read the dish back from the database
        dish_from_db = await crud_dish.read_dish(session, dish_id, submenu_id, menu_id)

        assert dish_from_db.title == dish_in.title
        assert dish_from_db.description == dish_in.description
        assert dish_from_db.price == dish_in.price

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_update_dish(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id

        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price='10.00')
        dish = await crud_dish.create_dish(session, dish_in, submenu_id, menu_id)
        dish_id = dish.id

        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Update the dish
        dish_update = DishBase(title="Updated Dish", description="not a yoghurt", price='20.00')
        updated_dish = await crud_dish.update_dish(session, dish_id, dish_update, submenu_id, menu_id)

        assert updated_dish.title == dish_update.title
        assert updated_dish.description == dish_update.description
        assert updated_dish.price == dish_update.price

        # cleanup
        await crud_menu.del_menu(session, menu_id)

@pytest.mark.asyncio
async def test_delete_dish(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu
        menu_in = MenuBase(title="Test Menu", description="Menu description")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        # Create submenu
        submenu_in = SubMenuBase(title="Test SubMenu", description="Submenu description")
        db_submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = db_submenu.id

        # Create a new dish
        dish_in = DishBase(title="Test Dish", description="Yoghurt", price='10.00')
        dish = await crud_dish.create_dish(session, dish_in, submenu_id, menu_id)
        dish_id = dish.id


        assert dish.title == dish_in.title
        assert dish.description == dish_in.description
        assert dish.price == dish_in.price

        # Delete the dish
        delete_response = await crud_dish.del_dish(session, dish_id, submenu_id, menu_id)

        # Check if the deletion was successful
        assert delete_response == {"message": f"Dish {dish.id} deleted successfully."}

        # Expect an HTTPException
        with pytest.raises(HTTPException):
            await crud_dish.read_dish(session, dish.id, submenu_id, menu_id)

        # cleanup
        await crud_menu.del_menu(session, menu_id)
