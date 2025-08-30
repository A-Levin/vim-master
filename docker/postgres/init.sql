-- Инициализация базы данных VimMaster
-- Создание дополнительных расширений если нужно

-- Включение расширений PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Создание типов данных
CREATE TYPE quest_type_enum AS ENUM (
    'command',
    'sequence', 
    'challenge',
    'macro',
    'navigation',
    'editing',
    'search_replace'
);

CREATE TYPE progress_status_enum AS ENUM (
    'not_started',
    'in_progress',
    'completed',
    'mastered',
    'skipped'
);

CREATE TYPE achievement_type_enum AS ENUM (
    'quest_completion',
    'streak',
    'speed',
    'efficiency',
    'exploration',
    'mastery'
);

-- Настройки для производительности
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET pg_stat_statements.max = 10000;
ALTER SYSTEM SET pg_stat_statements.track = all;

-- Комментарий для документации
COMMENT ON DATABASE vim_master_db IS 'VimMaster educational game database';