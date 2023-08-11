# docker
SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://ylab:no_secure_password@db/resto'
URL = 'http://web:8000'


def reverse_url(route_name: str, **kwargs) -> str:
    routes = {
        'all': '/api/v1/all',
        'get_menus': '/api/v1/menus',
        'post_menu': '/api/v1/menus',
        'get_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'patch_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'delete_menu': f'/api/v1/menus/{kwargs.get("menu_id", "")}',
        'get_menu_orm': f'/api/v1/menus/ORM/{kwargs.get("menu_id", "")}',
        'get_submenus': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'post_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus',
        'get_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'patch_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'delete_submenu': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}',
        'get_dishes': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'post_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/{kwargs.get("submenu_id", "")}/dishes',
        'get_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                    f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'patch_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                      f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
        'delete_dish': f'/api/v1/menus/{kwargs.get("menu_id", "")}/submenus/'
                       f'{kwargs.get("submenu_id", "")}/dishes/{kwargs.get("dish_id", "")}',
    }

    return str(routes.get(route_name))
