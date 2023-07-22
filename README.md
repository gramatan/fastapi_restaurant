# fastapi_restaurant

## Как запустить проект

1. Клонируйте репозиторий:

```bash
git clone https://github.com/gramatan/fastapi_restaurant.git
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv
```

3. Активируйте виртуальное окружение:

- Linux/macOS:

```bash
source venv/bin/activate
```

- Windows:

```cmd
.\venv\Scripts\activate
```

4. Установите необходимые пакеты:

```bash
pip install -r requirements.txt
```

5. Запустите Docker:

```bash
docker-compose up
```

6. Создайте таблицы в базе данных(в соседнем терминале или остановив docker-compose.):

```bash
python create_tables.py
```
7. Если вы выбрали остановку docker-compose, то запустите его снова:

```bash
docker-compose up
```

Всё готово! Теперь вы готовы приступить к тестированию!
