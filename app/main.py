import logging
import os

from celery import Celery
from fastapi import FastAPI

from app.routers import dish_router, menu_router, submenu_router

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(menu_router.router, prefix='/api/v1', tags=['menus'])
app.include_router(submenu_router.router, prefix='/api/v1/menus/{menu_id}', tags=['submenus'])
app.include_router(dish_router.router, prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['dishes'])

celery_app = Celery('resto')
celery_app.config_from_object('celery_config')

try:
    task_flag = os.environ.get('RUN_BACKGROUND_TASK')
except KeyError:
    task_flag = 'False'

if os.environ.get('RUN_BACKGROUND_TASK') == 'True':
    pass
    # TODO: задачку на запуск чтения меню из файла в базу данных сделать должен ты

logging.info(f'!!!Background task=={task_flag}')
