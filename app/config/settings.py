"""Application settings and configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    debug: bool = Field(default=False, description="Enable debug mode")
    secret_key: str = Field(
        default="your-super-secret-key-change-this-in-production",
        description="Secret key for JWT tokens",
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration time in minutes"
    )

    # Telegram Bot
    telegram_bot_token: str = Field(
        default="", description="Telegram bot token from @BotFather"
    )
    telegram_webhook_url: str | None = Field(
        default=None, description="Webhook URL for Telegram bot"
    )
    telegram_webhook_secret_token: str | None = Field(
        default=None, description="Secret token for webhook validation"
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://vim_master:password@localhost:5432/vim_master_db",
        description="Database connection URL",
    )
    database_host: str = Field(default="localhost", description="Database host")
    database_port: int = Field(default=5432, description="Database port")
    database_name: str = Field(default="vim_master_db", description="Database name")
    database_user: str = Field(default="vim_master", description="Database user")
    database_password: str = Field(default="password", description="Database password")

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")

    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=False, description="Enable API auto-reload")

    # CORS
    allowed_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "https://your-frontend-domain.com",
        ],
        description="Allowed CORS origins",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json/text)")

    # Game Configuration
    max_hints_per_quest: int = Field(default=3, description="Maximum hints per quest")
    default_quest_time_limit: int = Field(
        default=300, description="Default quest time limit in seconds"
    )
    streak_reset_hours: int = Field(
        default=48, description="Hours after which streak resets"
    )
    leaderboard_size: int = Field(
        default=100, description="Number of users in leaderboard"
    )

    # Telegram Mini App
    mini_app_url: str | None = Field(default=None, description="Telegram Mini App URL")
    mini_app_secret: str | None = Field(
        default=None, description="Mini App secret for validation"
    )

    # Monitoring
    sentry_dsn: str | None = Field(
        default=None, description="Sentry DSN for error monitoring"
    )

    # Testing
    test_database_url: str | None = Field(default=None, description="Test database URL")

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug

    def get_database_url(self, test: bool = False) -> str:
        """Get database URL for normal or test environment."""
        if test and self.test_database_url:
            return self.test_database_url
        return self.database_url


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return settings
