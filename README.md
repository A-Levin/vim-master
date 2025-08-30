# VimMaster 🎮

**Образовательная Telegram игра для изучения Vim команд**

VimMaster — это интерактивная игра-квест в Telegram, которая помогает изучить редактор Vim через практические задания. Пользователи проходят квесты, изучают команды и зарабатывают очки, соревнуясь с другими игроками.

## 🚀 Особенности

- **📚 Обучающие квесты** — Пошаговое изучение Vim от базовых команд до продвинутых
- **🎯 Интерактивные задания** — Реальные сценарии использования Vim
- **🏆 Система достижений** — Очки, уровни и соревнования
- **📱 Telegram Mini App** — Современный веб-интерфейс для углубленного изучения
- **🤖 Умный бот** — Автоматическая проверка команд и подсказки

## 🏗️ Архитектура

### Технологический стек

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Bot**: aiogram 3.x
- **Database**: PostgreSQL / SQLite
- **Cache**: Redis
- **Frontend**: Vue.js (для Mini App)
- **DevOps**: Docker, GitHub Actions, pre-commit hooks

### Структура проекта

```
vim-master/
├── app/                     # Основное приложение
│   ├── api/                # FastAPI endpoints для Mini App
│   ├── bot/                # Telegram Bot handlers
│   ├── core/               # Бизнес-логика (сервисы)
│   ├── db/                 # База данных (модели, репозитории)
│   ├── config/             # Конфигурации
│   └── tests/              # Тесты (unit/integration)
├── scripts/                # Служебные скрипты
├── .github/workflows/      # CI/CD пайплайны
├── docker/                 # Docker конфигурации
└── frontend/               # Vue.js Mini App (будущее)
```

## 🎮 Игровая механика

### MVP Квесты

1. **Dot Command** — Изучение точечной команды (.) для повторения действий
2. **Basic Motions** — Базовые движения: w, b, e
3. **Insert Mode Mastery** — Режимы вставки: A, I, o
4. **Visual Selection** — Визуальный режим и операции
5. **Search & Replace** — Поиск и замена текста

### Система скоринга

- **Базовые очки** за правильный ответ
- **Штрафы** за дополнительные попытки
- **Бонусы** за скорость выполнения
- **Подсказки** снижают итоговый счет

### Прогресс игрока

- **Уровни** в зависимости от общих очков
- **Статистика** завершенных квестов
- **Достижения** за особые успехи
- **Рейтинги** среди других игроков

## 🛠️ Быстрый старт

### Установка и запуск

1. **Клонирование репозитория:**
```bash
git clone https://github.com/A-Levin/vim-master.git
cd vim-master
```

2. **Установка зависимостей:**
```bash
# Установка uv (быстрый менеджер пакетов Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установка зависимостей проекта
uv sync
```

3. **Настройка окружения:**
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование конфигурации
nano .env
```

4. **Создание базы данных:**
```bash
# Создание таблиц
uv run python scripts/seed_quests.py
```

5. **Запуск приложения:**
```bash
# Только бот
uv run python app/main.py

# FastAPI + Bot
uv run uvicorn app.main:app --reload
```

### Docker запуск

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f vim-master-bot
```

## 🔧 Конфигурация

### Основные настройки (.env)

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=ваш_токен_от_@BotFather

# База данных
DATABASE_URL=postgresql://user:password@localhost/vim_master_db

# Redis (опционально)
REDIS_URL=redis://localhost:6379/0

# API настройки
API_HOST=0.0.0.0
API_PORT=8000

# Разработка
DEBUG=true
LOG_LEVEL=INFO
```

### Регистрация Telegram Bot

1. Отправьте `/newbot` боту @BotFather
2. Выберите имя и username для бота
3. Получите токен и добавьте в `.env`
4. Настройте команды бота:
```
start - Начать игру
profile - Мой профиль
quest - Новый квест
help - Помощь
```

## 🧪 Разработка

### Команды для разработки

```bash
# Установка dev зависимостей
uv sync --dev

# Запуск тестов
uv run pytest

# Проверка кода
uv run ruff check app/
uv run ruff format app/
uv run mypy app/

# Установка pre-commit hooks
uv run pre-commit install

# Создание миграций (будущее)
uv run alembic revision --autogenerate -m "описание"
uv run alembic upgrade head
```

### Структура тестов

```bash
app/tests/
├── unit/                   # Unit тесты
│   ├── test_config.py
│   └── test_keyboards.py
├── integration/            # Интеграционные тесты
│   ├── test_database.py
│   ├── test_bot_handlers.py
│   └── test_main.py
└── conftest.py            # Общие фикстуры
```

### Добавление нового квеста

1. **Создайте квест в базе:**
```python
quest = Quest(
    chapter_id=chapter.id,
    title="Название квеста",
    description="Описание задания",
    quest_type=QuestType.COMMAND,
    difficulty=DifficultyLevel.BEGINNER,
    initial_text="исходный текст",
    expected_result="ожидаемый результат", 
    vim_command="команда_vim",
    hints=["подсказка 1", "подсказка 2"],
    max_score=15,
    time_limit=90
)
```

2. **Обновите валидацию команд** в `QuestService`
3. **Добавьте тесты** для нового квеста

## 🤝 API Documentation

### Основные endpoints

**Аутентификация:**
- `POST /api/v1/auth/login` — Логин через Telegram
- `GET /api/v1/auth/me` — Информация о текущем пользователе

**Квесты:**
- `GET /api/v1/quests/chapters` — Список глав
- `GET /api/v1/quests/chapters/{id}/quests` — Квесты главы
- `POST /api/v1/quests/{id}/start` — Начать квест
- `POST /api/v1/quests/submit` — Отправить ответ
- `GET /api/v1/quests/recommended` — Рекомендуемый квест

**Прогресс:**
- `GET /api/v1/progress/summary` — Общая статистика
- `GET /api/v1/progress/completed` — Завершенные квесты

Полная документация доступна на `/docs` при запущенном сервере.

## 🔄 CI/CD

### GitHub Actions Workflow

Автоматические проверки при каждом push/PR:

- **Линтинг** — ruff check и format
- **Типы** — mypy проверки
- **Тесты** — unit и integration тесты
- **Покрытие** — отчеты покрытия кода

### Pre-commit Hooks

Локальные проверки перед коммитом:
- Форматирование кода
- Проверка типов
- Unit тесты
- Проверка YAML файлов

## 📊 Мониторинг и логи

### Логирование

```python
# Настройка в settings.py
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=json # json, text

# В коде
import logging
logger = logging.getLogger(__name__)
logger.info("Квест начат", extra={"user_id": user.id, "quest_id": quest.id})
```

### Метрики (планируется)

- Количество активных пользователей
- Завершенные квесты по дням
- Средний score по квестам
- Время выполнения квестов

## 🚢 Развертывание

### Production окружение

1. **Настройте переменные окружения:**
```bash
DEBUG=false
DATABASE_URL=postgresql://user:pass@db:5432/vim_master
REDIS_URL=redis://redis:6379/0
SENTRY_DSN=https://sentry.io/dsn
```

2. **Используйте Docker Compose:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Настройте reverse proxy** (nginx/traefik)
4. **Настройте SSL сертификаты**
5. **Настройте автоматические бэкапы БД**

### Масштабирование

- **Горизонтальное масштабирование** FastAPI через load balancer
- **Шардинг базы данных** по пользователям
- **Redis Cluster** для кеширования
- **CDN** для статических файлов Mini App

## 🤝 Вклад в проект

### Как помочь проекту

1. **🐛 Сообщайте о багах** через GitHub Issues
2. **💡 Предлагайте новые квесты** и идеи
3. **📝 Улучшайте документацию**
4. **🧪 Пишите тесты**
5. **🌍 Переводите на другие языки**
6. **💰 Поддержите проект финансово** (см. раздел "Донаты")

### Процесс разработки

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения с тестами
4. Убедитесь что проходят все проверки
5. Создайте Pull Request

### Стандарты кода

- **Python**: PEP 8, type hints обязательны
- **Коммиты**: Conventional Commits format
- **Тесты**: Покрытие новой функциональности
- **Документация**: Docstrings для всех публичных функций

## 📝 TODO и Roadmap

### Ближайшие планы (v0.2)

- [ ] **Telegram Mini App** — Vue.js интерфейс
- [ ] **Больше квестов** — 20+ квестов по всем аспектам Vim
- [ ] **Система рейтингов** — Глобальные и еженедельные лидерборды  
- [ ] **Социальные функции** — Друзья, соревнования, команды
- [ ] **Достижения** — Бейджи и награды за особые успехи

### Долгосрочные планы (v1.0)

- [ ] **Мультиязычность** — Поддержка 5+ языков
- [ ] **AI-помощник** — Персонализированные подсказки
- [ ] **Vim конфигуратор** — Помощь в настройке .vimrc
- [ ] **Интеграция с редакторами** — VS Code, Neovim плагины
- [ ] **Мобильное приложение** — Native iOS/Android

### Контент планы

- [ ] **Vim Plugins** — Изучение популярных плагинов
- [ ] **Advanced Editing** — Макросы, регулярные выражения
- [ ] **Vim Scripting** — Основы vimscript
- [ ] **Neovim Features** — Lua конфигурация, LSP

## 💰 Поддержка проекта

VimMaster — это бесплатный open source проект, который развивается благодаря энтузиазму и поддержке сообщества. Если проект оказался полезным, вы можете поддержать его развитие:

### 🎯 На что идут донаты

- **🖥️ Серверные ресурсы** — Хостинг бота и API
- **💾 База данных** — PostgreSQL и Redis в облаке  
- **🔍 Мониторинг** — Sentry, логи, метрики
- **🌐 CDN** — Быстрая загрузка для Mini App
- **☕ Мотивация разработчика** — Кофе для продуктивной работы

### 💳 Способы поддержки

#### 🤖 Telegram (самый удобный способ!)
- **💎 Telegram Stars** — Встроенная система донатов в боте
- **🎁 Telegram Gifts** — Отправка подарков через @VimMasterBot
- **💰 TON Wallet** — `UQD...` (нативная крипта Telegram)

```
Просто напишите /donate в боте @VimMasterBot! 
```

#### 🔐 Криптовалюты (анонимно и быстро)
- **₿ Bitcoin (BTC)**: `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
- **Ξ Ethereum (ETH)**: `0x742d35Cc6634C0532925a3b8D58A37F39534BB26`
- **₮ USDT TRC20**: `TGhP4M8GGhjkXYZ...`
- **⚪ USDC (ERC20)**: `0x742d35Cc6634C0532925a3b8D58A37F39534BB26`
- **💎 TON**: `UQD4FPq-w0yog4wQrq0Q4FEikdHNjjL_VrKWy2LtuH44-QH7`

#### 🌍 Международные платформы
- **❤️ GitHub Sponsors**: [github.com/sponsors/A-Levin](https://github.com/sponsors/A-Levin)
- **☕ Buy Me a Coffee**: [buymeacoffee.com/alevin](https://buymeacoffee.com/alevin)
- **💝 Open Collective**: [opencollective.com/vim-master](https://opencollective.com/vim-master)

#### 🇷🇺 Российские сервисы
- **🥝 Qiwi**: [qiwi.com/n/ALEVIN](https://qiwi.com/n/ALEVIN)
- **💳 YooMoney**: `410011234567890`
- **🏦 Сбербанк**: `+7 (900) 123-45-67` 

### 🏆 Спонсоры проекта

**🥇 Золотые спонсоры ($100+/мес)**
- Ваше имя может быть здесь!

**🥈 Серебряные спонсоры ($50+/мес)**  
- Ваше имя может быть здесь!

**🥉 Бронзовые спонсоры ($10+/мес)**
- Ваше имя может быть здесь!

### 🎁 Бонусы для спонсоров

- **📛 Специальный бейдж** в Telegram боте
- **🌟 Имя в разделе спонсоров** в README
- **💡 Приоритет предложений** новых функций
- **🎯 Эксклюзивные квесты** для спонсоров
- **📞 Прямая связь** с разработчиком

### 💪 Другие способы помочь

Не можете поддержать финансово? Вот другие способы помочь:

- ⭐ **Поставьте звезду** на GitHub
- 📢 **Расскажите о проекте** друзьям и коллегам
- 🐦 **Поделитесь в соцсетях** #VimMaster #LearnVim
- 📝 **Напишите отзыв** или статью о проекте
- 🎥 **Создайте видео** с обзором или туториалом
- 🌍 **Переведите на свой язык**

**Каждый донат мотивирует на дальнейшую разработку!** ❤️

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 👥 Авторы

- **Abdullah Levin** - *Initial work* - [A-Levin](https://github.com/A-Levin)

## 🙏 Благодарности

- **Vim Community** — За потрясающий редактор
- **aiogram** — Отличная библиотека для Telegram ботов
- **FastAPI** — Современный и быстрый веб-фреймворк
- **Claude Code** — За помощь в разработке архитектуры

---

**Сделано с ❤️ для Vim сообщества**

Если проект помог вам изучить Vim — поставьте ⭐ на GitHub!