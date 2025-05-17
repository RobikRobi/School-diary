📘 School Diary
1. 📄 Description

School Diary — это backend-сервис для электронной школьной системы. Он управляет пользователями, предметами, оценками и расписанием, предоставляет API для frontend-интерфейсов и административной панели, а также поддерживает WebSocket для обновлений в реальном времени.
2. 🚀 Getting Started
🧾 Установка (локально)

Клонируйте репозиторий:

```powershell
git clone https://github.com/RobikRobi/School-diary.git
cd School-diary
```

Установите зависимости:
```
pip install --upgrade pip
pip install -r requirements.txt
```
Создайте .env файл:

```.env
DB_URL=sqlite:///./mydatabase.db
DB_URL_ASYNC=sqlite+aiosqlite:///./mydatabase.db
```

Запуск:

```powershell
uvicorn src.main:app --reload
```

Открой: http://localhost:8000
🐳 Запуск в Docker

```powershell
docker build -t school-diary .
docker run -d -p 8000:8000 --env-file .env school-diary
```

3. 🏗️ Architecture

School-diary/
├── src/
│   ├── main.py           # Точка входа в FastAPI
│   ├── config.py         # Конфигурация через pydantic-settings
│   ├── db.py             # Инициализация базы данных
│   ├── models/           # SQLAlchemy ORM модели (User, Mark, Subject и т.д.)
│   ├── routers/          # API endpoints
│   └── websocket/        # WebSocket обработка оценок
├── requirements.txt      # Зависимости проекта
├── Dockerfile            # Docker-инструкция
└── .env                  # Переменные окружения

3.2 💻 Code Style

Код оформляется в соответствии с PEP8 + FastAPI best practices.
3.2.1 📥 Imports

Импорты структурированы по следующему шаблону:

# Стандартная библиотека
import os

# Сторонние зависимости
from fastapi import FastAPI

# Внутренние модули
from src.models import User

3.2.2 🧹 Code Linter

Рекомендуемые инструменты:

    black — автоформатирование

    flake8 — проверка стиля

    isort — сортировка импортов

    mypy — статическая проверка типов

Установка (опционально):

pip install black flake8 isort mypy

3.2.3 🔮 Future Features

   - [ ] 🔐 Авторизация и роли пользователей (ученик, учитель, админ)

   - [ ] 📈 Получение статистики успеваемости

   - [ ] 🗓️ Гибкое управление расписанием

   - [ ] 💬 Поддержка уведомлений через WebSocket

   - [ ] ☁️ Перевод на PostgreSQL и деплой на облачный хостинг
