# fastapi_restaurant

0. Клонируйте репозиторий:

```bash
git clone https://github.com/gramatan/fastapi_restaurant.git
```
## Для запуска проекта без pytest:
1. Находясь в папке с проектом выполните:

```bash
docker-compose up
```

## Для запуска проекта и тестов в отдельном контейнере:
1. Находясь в папке с проектом выполните:

```bash
docker-compose -f docker-compose-test.yaml up
```

Результаты тестов будут отображены в консоли.

Оба варианта светят в одинаковые порты, поэтому при запуске одного из вариантов, второй должен быть выключен.

Всё готово к тестированию!

Приложение доступно на 8000 порту.
Основной исполняемый файл: /app/main.py

Тесты находятся в папке app/tests. Сценарий "Проверка количества блюд и подменю в меню" находится в файле [test_api_postman_count.py](app%2Ftests%2Ftest_api_postman_count.py)

[test_api_second_part.py](app%2Ftests%2Ftest_api_second_part.py) - все остальные проверки api.

CRUD тесты находятся в файлах:
[test_lists.py](app%2Ftests%2Ftest_lists.py)
[test_menus.py](app%2Ftests%2Ftest_menus.py)
[test_submenus.py](app%2Ftests%2Ftest_submenus.py)
[test_dishes.py](app%2Ftests%2Ftest_dishes.py)

Очистить таблицы можно запустив файл create_tables.py (по умолчанию база пустая и готова к работе).
