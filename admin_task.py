import openpyxl

from app.repository.admin import (
    create_dish,
    create_menu,
    create_submenu,
    del_dish,
    del_menu,
    del_submenu,
    dish_exists,
    menu_exists,
    submenu_exists,
    update_dish,
    update_menu,
    update_submenu,
)

MenuType = list[tuple[int, str, str]]
SubMenuType = list[tuple[int, int, str, str]]
DishType = list[tuple[int, int, int, str, str, str]]
GLOBAL_DATA: dict[str, list]

GLOBAL_DATA = {
    'menus': [],
    'submenus': [],
    'dishes': []
}


async def read_excel_to_data(filename: str) -> dict[str, list]:
    """
    Чтение файла Excel и преобразование его в нужный формат данных.
    """
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active

    menus = []
    submenus = []
    dishes = []

    last_menu_id = None
    last_submenu_id = None

    for row in sheet.iter_rows(values_only=True):
        if row[0] is not None:  # Это меню
            last_menu_id = row[0]
            menus.append((row[0], row[1], row[2]))
        elif row[1] is not None:  # Это подменю
            last_submenu_id = row[1]
            submenus.append((last_menu_id, row[1], row[2], row[3]))
        else:  # Это блюдо
            dishes.append((last_menu_id, last_submenu_id, row[2], row[3], row[4], row[5]))

    return {'menus': menus, 'submenus': submenus, 'dishes': dishes}


async def compare_data(new_data: dict[str, list]) -> dict[str, tuple[list, list]]:
    """
    Сравнивает новые данные с глобальной переменной и составляет списки для CRUD-операций.
    """
    menus_to_create_or_update = [menu for menu in new_data['menus'] if (menu not in GLOBAL_DATA['menus']) or (
        menu in GLOBAL_DATA['menus'] and menu != GLOBAL_DATA['menus'][GLOBAL_DATA['menus'].index(menu)])]

    menus_to_delete = [menu for menu in GLOBAL_DATA['menus'] if menu not in new_data['menus']]

    submenus_to_create_or_update = [submenu for submenu in new_data['submenus'] if (submenu not in GLOBAL_DATA['submenus']) or (
        submenu in GLOBAL_DATA['submenus'] and submenu != GLOBAL_DATA['submenus'][GLOBAL_DATA['submenus'].index(submenu)])]
    submenus_to_delete = [submenu for submenu in GLOBAL_DATA['submenus'] if submenu not in new_data['submenus']]

    dishes_to_create_or_update = [dish for dish in new_data['dishes'] if (dish not in GLOBAL_DATA['dishes']) or (
        dish in GLOBAL_DATA['dishes'] and dish != GLOBAL_DATA['dishes'][GLOBAL_DATA['dishes'].index(dish)])]
    dishes_to_delete = [dish for dish in GLOBAL_DATA['dishes'] if dish not in new_data['dishes']]

    result = {
        'menus': (menus_to_create_or_update, menus_to_delete),
        'submenus': (submenus_to_create_or_update, submenus_to_delete),
        'dishes': (dishes_to_create_or_update, dishes_to_delete)
    }
    return result


async def process_crud(compared_data: dict[str, tuple[list, list]]):
    print(compared_data)

    for menu in compared_data['menus'][0]:
        manual_id = f'{menu[0]}'
        exists = await menu_exists(manual_id)
        if exists:
            await update_menu(manual_id, menu)
        else:
            await create_menu(menu, manual_id)

    for menu in compared_data['menus'][1]:
        manual_id = f'{menu[0]}'
        exists = await menu_exists(manual_id)
        if exists:
            await del_menu(manual_id)

    for submenu in compared_data['submenus'][0]:
        manual_id = f'{submenu[0]}:{submenu[1]}'
        exists = await submenu_exists(manual_id)
        if exists:
            await update_submenu(manual_id, submenu)
        else:
            await create_submenu(submenu, manual_id)

    for submenu in compared_data['submenus'][1]:
        manual_id = f'{submenu[0]}:{submenu[1]}'
        exists = await submenu_exists(manual_id)
        if exists:
            await del_submenu(manual_id)

    for dish in compared_data['dishes'][0]:
        manual_id = f'{dish[0]}:{dish[1]}:{dish[2]}'
        exists = await dish_exists(manual_id)
        if exists:
            await update_dish(manual_id, dish)
        else:
            await create_dish(dish, manual_id)

    for dish in compared_data['dishes'][1]:
        manual_id = f'{dish[0]}:{dish[1]}:{dish[2]}'
        exists = await dish_exists(manual_id)
        if exists:
            await del_dish(manual_id)


async def main():
    new_data = await read_excel_to_data('admin/Menu.xlsx')
    compared = await compare_data(new_data)
    await process_crud(compared)
    GLOBAL_DATA.update(new_data)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
