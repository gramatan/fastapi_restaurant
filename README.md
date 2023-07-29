# fastapi_restaurant
## Начало работы

### Клонирование репозитория

```bash
git clone https://github.com/gramatan/fastapi_restaurant.git
```

## Запуск проекта

### Без pytest

1. Перейдите в директорию проекта и выполните:

```bash
docker-compose up
```

### С pytest в отдельном контейнере

1. Перейдите в директорию проекта и выполните:

```bash
docker-compose -f docker-compose-test.yaml up
```

Результаты тестов будут отображены в консоли.

**Примечание:** Оба варианта используют одни и те же порты, поэтому при запуске одного из них, другой должен быть остановлен.

## Тестирование

Приложение готово к тестированию! Оно доступно на порту 8000. Основной исполняемый файл находится по адресу `/app/main.py`.

Тесты находятся в директории `app/tests`. Сценарий "Проверка количества блюд и подменю в меню" находится в файле [test_api_postman_count.py](app%2Ftests%2Ftest_api_postman_count.py).

Все остальные проверки API находятся в [test_api_second_part.py](app%2Ftests%2Ftest_api_second_part.py).

Тесты CRUD находятся в следующих файлах:
- [test_lists.py](app%2Ftests%2Ftest_lists.py)
- [test_menus.py](app%2Ftests%2Ftest_menus.py)
- [test_submenus.py](app%2Ftests%2Ftest_submenus.py)
- [test_dishes.py](app%2Ftests%2Ftest_dishes.py)

Подсчет количества подменю и блюд без использования полей реализован в [calc_submenu_and_dishes.py](app%2Fcrud%2Fcalc_submenu_and_dishes.py). Он доступен через конечную точку **`get("/api/v1/menu/{menu_id}")`**.

## База данных

Вы можете очистить таблицы, запустив файл `create_tables.py`. По умолчанию база данных пуста и готова к использованию.

При запуске через тесты для базы данных не предусмотрен именованный том, поэтому данные будут потеряны при перезапуске контейнера.