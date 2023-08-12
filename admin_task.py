import asyncio
import json
import os
from datetime import timedelta

import openpyxl
from celery import Celery

from app.repository.admin import (
    check_and_del_dish,
    check_and_del_menu,
    check_and_del_submenu,
    create_update_dish,
    create_update_menu,
    create_update_submenu,
)

MenuType = list[tuple[int, str, str]]
SubMenuType = list[tuple[int, int, str, str]]
DishType = list[tuple[int, int, int, str, str, str]]
GLOBAL_DATA: dict[str, list]

global_data_path = 'global_data.json'


def load_global_data():
    if os.path.exists(global_data_path):
        try:
            with open(global_data_path, encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'Error loading global data: {e}')
            return {'menus': [], 'submenus': [], 'dishes': []}
    return {'menus': [], 'submenus': [], 'dishes': []}


def save_global_data(data: dict[str, list]):
    try:
        with open(global_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f'Error saving global data: {e}')


GLOBAL_DATA = load_global_data()


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
            menus.append([row[0], row[1], row[2]])
        elif row[1] is not None:  # Это подменю
            last_submenu_id = row[1]
            submenus.append([last_menu_id, row[1], row[2], row[3]])
        else:  # Это блюдо
            dishes.append([last_menu_id, last_submenu_id, row[2], row[3], row[4], row[5]])

    return {'menus': menus, 'submenus': submenus, 'dishes': dishes}


def get_manual_id_from_data(item, data_type):
    if data_type == 'menus':
        return item[0]
    elif data_type == 'submenus':
        return f'{item[0]}:{item[1]}'
    elif data_type == 'dishes':
        return f'{item[0]}:{item[1]}:{item[2]}'
    else:
        return None


async def compare_data(new_data: dict[str, list]) -> dict[str, list]:
    result = {}

    for data_type in ['menus', 'submenus', 'dishes']:
        old_manual_ids = {get_manual_id_from_data(item, data_type): item for item in GLOBAL_DATA[data_type]}
        new_manual_ids = {get_manual_id_from_data(item, data_type): item for item in new_data[data_type]}

        to_delete = [item for manual_id, item in old_manual_ids.items() if manual_id not in new_manual_ids]
        to_create = [item for manual_id, item in new_manual_ids.items() if manual_id not in old_manual_ids]

        to_update = [new_item for manual_id, new_item in new_manual_ids.items() if
                     manual_id in old_manual_ids and new_item != old_manual_ids[manual_id]]

        result[data_type] = [to_create + to_update, to_delete]

    return result


async def process_crud(compared_data: dict[str, list]):
    # Menus
    for menu in compared_data['menus'][0]:
        manual_id = f'{menu[0]}'
        await create_update_menu(menu, manual_id)

    for menu in compared_data['menus'][1]:
        manual_id = f'{menu[0]}'
        await check_and_del_menu(manual_id)

    # Submenus
    for submenu in compared_data['submenus'][0]:
        manual_id = f'{submenu[0]}:{submenu[1]}'
        await create_update_submenu(submenu, manual_id)

    for submenu in compared_data['submenus'][1]:
        manual_id = f'{submenu[0]}:{submenu[1]}'
        await check_and_del_submenu(manual_id)

    # Dishes
    for dish in compared_data['dishes'][0]:
        manual_id = f'{dish[0]}:{dish[1]}:{dish[2]}'
        await create_update_dish(dish, manual_id)

    for dish in compared_data['dishes'][1]:
        manual_id = f'{dish[0]}:{dish[1]}:{dish[2]}'
        await check_and_del_dish(manual_id)


celery_app = Celery('admin_task')

celery_app.conf.update(
    broker_url='pyamqp://guest:guest@rabbitmq:5672//',
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Moscow',
    enable_utc=True,
    beat_schedule={
        'main': {
            'task': 'admin_task.main',
            'schedule': timedelta(seconds=15),
        },
    }
)


async def main_async():
    """
    Основная функция, которая выполняется в Celery.
    """
    new_data = await read_excel_to_data('admin/Menu.xlsx')
    print(f'new_data = {new_data}')
    compared = await compare_data(new_data)
    await process_crud(compared)

    to_save = {
        'menus': new_data['menus'],
        'submenus': new_data['submenus'],
        'dishes': new_data['dishes']
    }

    # debug purposes
    save_global_data(to_save)
    GLOBAL_DATA_test = load_global_data()
    print(f'global = {GLOBAL_DATA_test}')


@celery_app.task
def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_async())


if __name__ == '__main__':
    asyncio.run(main_async())
