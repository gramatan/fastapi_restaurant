# fastapi_restaurant

## До начала
* Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос. - в репозитории menu
[menu.py](app%2Frepository%2Fmenu.py) - orm_read_menu
* Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest -
сценарий использовался в тестах: [test_api_all.py](app%2Ftests%2Ftest_api_all.py)
* Описать ручки API в соответствий c OpenAPI - [openapi.json](openapi.json)
* Реализовать в тестах аналог Django reverse() для FastAPI - [conftest.py](app%2Ftests%2Fconftest.py) - функция reverse_url


* Фоновая задача: синхронизация Excel документа и БД. - [admin_task.py](admin_task.py)
  репо к ней:[admin.py](app%2Frepository%2Fadmin.py)
* Доступная наружу папка(имя файла - хардкод) [admin](admin)

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

Тесты находятся в директории `app/tests`.

Все тесты API находятся в [test_api_all.py](app%2Ftests%2Ftest_api_all.py) и используют reverse_url() для получения адресов.
Все тесты из сценария "Проверка количества блюд и подменю в меню" входят в общий список тестов.

Подсчет количества подменю и блюд без использования полей реализован в [menu.py](app%2Frepository%2Fmenu.py).
Он доступен через конечную точку **`get("/api/v1/menus/ORM/{menu_id}")`**.

[openapi.json](openapi.json) содержит описание API.

## База данных

Вы можете очистить таблицы, запустив файл `create_tables.py`. По умолчанию база данных пуста и готова к использованию.

При запуске через тесты для базы данных не предусмотрен именованный том, поэтому данные будут потеряны при перезапуске контейнера.
