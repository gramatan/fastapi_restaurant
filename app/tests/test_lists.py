import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.crud import dish as crud_dish
from app.crud import menu as crud_menu
from app.crud import submenu as crud_submenu
from app.schemas import MenuBase, SubMenuBase, DishBase
from app.database.base import SQLALCHEMY_DATABASE_URL


# Database fixture
@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        yield session


@pytest.mark.asyncio
async def test_empty_lists(db_session: AsyncSession) -> None:
    async for session in db_session:
        menus = await crud_menu.read_menus(session)
    async for session in db_session:
        submenus = await crud_submenu.read_submenus(session, 9999)
    async for session in db_session:
        dishes = await crud_dish.read_dishes(session, 9999, 9999)

        assert menus == []
        assert submenus == []
        assert dishes == []


@pytest.mark.asyncio
async def test_read_menus(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create two menus
        menu_in1 = MenuBase(title="Test Menu 1", description="This is test menu 1")
        menu1 = await crud_menu.create_menu(session, menu_in1)
        menu_id1 = menu1.id

        menu_in2 = MenuBase(title="Test Menu 2", description="This is test menu 2")
        menu2 = await crud_menu.create_menu(session, menu_in2)
        menu_id2 = menu2.id

        # Read menus
        menus = await crud_menu.read_menus(session)

        # Check if the menus are correctly returned
        assert len(menus) == 2
        assert menus[0].id == menu1.id
        assert menus[1].id == menu2.id

        # cleanup
        await crud_menu.del_menu(session, menu_id1)
        await crud_menu.del_menu(session, menu_id2)


@pytest.mark.asyncio
async def test_read_submenus(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu and two submenus
        menu_in = MenuBase(title="Test Menu", description="This is test menu")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        submenu_in1 = SubMenuBase(title="Test SubMenu 1", description="This is test submenu 1")
        submenu1 = await crud_submenu.create_submenu(session, submenu_in1, menu_id)

        submenu_in2 = SubMenuBase(title="Test SubMenu 2", description="This is test submenu 2")
        submenu2 = await crud_submenu.create_submenu(session, submenu_in2, menu_id)

        # Read submenus
        submenus = await crud_submenu.read_submenus(session, menu_id)

        # Check if the submenus are correctly returned
        assert len(submenus) == 2
        assert submenus[0].id == submenu1.id
        assert submenus[1].id == submenu2.id

        # cleanup
        await crud_menu.del_menu(session, menu_id)


@pytest.mark.asyncio
async def test_read_dishes(db_session: AsyncSession) -> None:
    async for session in db_session:
        # Create menu, submenu and two dishes
        menu_in = MenuBase(title="Test Menu", description="This is test menu")
        menu = await crud_menu.create_menu(session, menu_in)
        menu_id = menu.id

        submenu_in = SubMenuBase(title="Test SubMenu", description="This is test submenu")
        submenu = await crud_submenu.create_submenu(session, submenu_in, menu_id)
        submenu_id = submenu.id

        dish_in1 = DishBase(title="Test Dish 1", description="This is test dish 1", price='10.00')
        dish1 = await crud_dish.create_dish(session, dish_in1, submenu_id, menu_id)

        dish_in2 = DishBase(title="Test Dish 2", description="This is test dish 2", price='20.00')
        dish2 = await crud_dish.create_dish(session, dish_in2, submenu_id, menu_id)

        # Read dishes
        dishes = await crud_dish.read_dishes(session, submenu_id, menu_id)

        # Check if the dishes are correctly returned
        assert len(dishes) == 2
        assert dishes[0].id == dish1.id
        assert dishes[1].id == dish2.id

        # cleanup
        await crud_menu.del_menu(session, menu_id)
