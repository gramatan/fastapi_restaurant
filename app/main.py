import logging

from fastapi import FastAPI

from app.routers import menu_router, submenu_router, dish_router

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(menu_router.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(submenu_router.router, prefix="/api/v1/menus/{menu_id}/submenus", tags=["submenus"])
app.include_router(dish_router.router, prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dishes"])
