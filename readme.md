# TeamFinder

Веб-приложение для поиска команды и проектов. **Вариант задания: 2** (навыки пользователей и фильтрация по навыкам).

---

## Запуск через Docker (рекомендуется для проверки)

### Первый запуск

1. Запустите проект:

   docker compose up --build


   Флаг `-d` можно добавить для фонового режима: `docker compose up -d --build`.


2. Откройте в браузере: [http://localhost:8000](http://localhost:8000)

Данные для входа: `demo1@example.com` / `demo2@example.com`, пароль `pass12345`.

### Остановка

```bash
docker compose down
```

Данные сохраняются в томах `postgres_data`, `static_data`, `media_data`. Чтобы удалить все тома: `docker compose down -v`.

### Порт PostgreSQL

По умолчанию БД доступна с хоста на `localhost:5432`. Если порт занят, измените **слева** в `docker-compose.yml` (`"5433:5432"`) и `POSTGRES_PORT` в `.env`.

---

## Локальная разработка без Docker (опционально)

### 1. Виртуальное окружение

```bash
python3 -m venv venv
```

**Активация:**

- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (cmd): `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Файл `.env`

В корне проекта должен быть файл `.env`:

| Переменная | Назначение |
|------------|------------|
| **DJANGO_SECRET_KEY** | Секретный ключ Django |
| **DJANGO_DEBUG** | Режим отладки (`True` при разработке, `False` для проверки с Nginx) |
| **POSTGRES_DB** | Имя базы PostgreSQL |
| **POSTGRES_USER** | Пользователь PostgreSQL |
| **POSTGRES_PASSWORD** | Пароль PostgreSQL |
| **POSTGRES_HOST** | `localhost` при локальном Django; в Docker для приложения задаётся `db` |
| **POSTGRES_PORT** | Порт БД (по умолчанию `5432`) |

### 3. Только PostgreSQL в Docker

```bash
docker compose up -d db
```

### 4. Django на хосте

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

Сайт: [http://localhost:8000](http://localhost:8000) (без Nginx; при `DEBUG=True` медиа отдаёт Django)
