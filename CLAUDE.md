# CLAUDE.md - VimMaster Project Configuration

## Общие настройки проекта
- **Проект**: VimMaster - образовательная Telegram игра для изучения Vim
- **Технологии**: Python, aiogram 3.x, FastAPI, PostgreSQL, Redis, Vue.js
- **Архитектура**: Microservices (Bot + API + Mini App)

## Структура проекта
```
vim-master/
├── app/                    # Основное приложение
│   ├── __init__.py
│   ├── main.py            # FastAPI app + Bot entry point
│   ├── config/            # Конфигурации
│   ├── bot/               # Telegram Bot (aiogram)
│   ├── api/               # FastAPI для Mini App
│   ├── core/              # Бизнес логика (Game Engine, Services)
│   ├── db/                # База данных (Models, Repositories)
│   ├── utils/             # Утилиты
│   └── tests/             # Тесты
├── docker/                # Docker конфигурации
├── requirements/          # Python зависимости
├── scripts/               # Служебные скрипты
├── frontend/              # Vue.js Mini App (создастся позже)
├── .env.example           # Пример переменных окружения
├── pyproject.toml         # Poetry конфигурация
├── docker-compose.yml     # Docker services
└── README.md
```

## Технические требования
- **Python**: 3.11+
- **База данных**: PostgreSQL 15+ для основных данных
- **Кеширование**: Redis 7+ для сессий и быстрого доступа
- **Менеджер зависимостей**: uv (быстрый менеджер пакетов на Rust)
- **Контейнеризация**: Docker + Docker Compose

## Команды для разработки
```bash
# Установка зависимостей
uv sync

# Запуск в режиме разработки
uv run python app/main.py

# Тестирование
uv run pytest

# Форматирование кода
uv run black app/
uv run isort app/
uv run ruff check app/ --fix

# Проверка типов
uv run mypy app/

# Миграции базы данных
uv run alembic upgrade head
```

## MVP функциональность
1. **Telegram Bot**:
   - Регистрация пользователей
   - Система команд (/start, /profile, /quest)
   - Базовые квесты с проверкой ответов
   - Система очков и уровней

2. **База данных**:
   - Пользователи (users)
   - Главы книги (chapters) 
   - Квесты (quests)
   - Прогресс пользователей (user_progress)
   - Достижения (achievements)

3. **Game Engine**:
   - Валидация Vim команд
   - Система скоринга
   - Прогрессия уровней
   - Выдача подсказок

4. **API для Mini App**:
   - Аутентификация через Telegram
   - Получение квестов и прогресса
   - Отправка результатов

## Первые 5 квестов (MVP)
1. **Dot Command** - знакомство с точечной командой (.)
2. **Basic Motions** - движения w, b, e
3. **Insert Mode** - команды вставки A, I, o
4. **Visual Selection** - визуальный режим и операции
5. **Search & Replace** - базовый поиск и замена

## Настройки окружения
- Копировать `.env.example` в `.env`
- Настроить токен Telegram бота
- Настроить подключения к PostgreSQL и Redis
- Для разработки использовать Docker Compose

## Стандарты кодирования
- **Форматирование**: Black (88 символов)
- **Импорты**: isort с профилем black
- **Типизация**: mypy для проверки типов
- **Тестирование**: pytest с async поддержкой
- **Commits**: Conventional Commits

## CI/CD Pipeline
- **Pre-commit hooks**: black, isort, flake8, mypy
- **Testing**: pytest с покрытием кода
- **Docker**: автосборка образов
- **Deployment**: Docker Compose для prod/staging

## Связанные файлы
- [Technical Architecture](docs/architecture.md) - детальная архитектура
- [Database Schema](docs/database.md) - схема БД
- [Quest System](docs/quests.md) - система квестов
- [API Documentation](docs/api.md) - документация API

## TODO для MVP
- [x] Создать базовую структуру проекта
- [x] Настроить pyproject.toml с зависимостями
- [ ] Создать Docker Compose для dev окружения
- [ ] Настроить базовые конфигурации (settings.py)
- [ ] Создать модели базы данных
- [ ] Реализовать базовый Telegram бот
- [ ] Создать первые 5 квестов
- [ ] Добавить систему аутентификации
- [ ] Создать API endpoints для Mini App
- [ ] Написать тесты для основной функциональности

## Правила разработки
- **ВСЕГДА** использовать type hints
- **ВСЕГДА** писать docstrings для публичных функций
- **ВСЕГДА** покрывать новый код тестами
- **НИКОГДА** не коммитить secrets в код
- **ОБЯЗАТЕЛЬНО** следовать архитектурным слоям (Repository -> Service -> Handler)

---
**Статус проекта**: 🚧 В активной разработке (MVP фаза)