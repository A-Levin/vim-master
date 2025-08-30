"""Unit tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from app.config.settings import Settings

pytestmark = pytest.mark.unit


class TestSettings:
    """Test Settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()

        assert settings.debug is False
        assert settings.secret_key == "your-super-secret-key-change-this-in-production"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30
        assert settings.api_host == "0.0.0.0"
        assert settings.api_port == 8000
        assert settings.log_level == "INFO"

    def test_settings_from_env(self):
        """Test settings loaded from environment variables."""
        with patch.dict(
            os.environ,
            {
                "DEBUG": "true",
                "SECRET_KEY": "test-secret",
                "TELEGRAM_BOT_TOKEN": "123456:test_token",
                "DATABASE_URL": "postgresql://test:test@localhost/test",
                "LOG_LEVEL": "DEBUG",
            },
        ):
            settings = Settings()

            assert settings.debug is True
            assert settings.secret_key == "test-secret"
            assert settings.telegram_bot_token == "123456:test_token"
            assert settings.database_url == "postgresql://test:test@localhost/test"
            assert settings.log_level == "DEBUG"

    def test_is_development_property(self):
        """Test is_development property."""
        settings = Settings(debug=True)
        assert settings.is_development is True

        settings = Settings(debug=False)
        assert settings.is_development is False

    def test_is_production_property(self):
        """Test is_production property."""
        settings = Settings(debug=True)
        assert settings.is_production is False

        settings = Settings(debug=False)
        assert settings.is_production is True

    def test_get_database_url_normal(self):
        """Test get_database_url for normal environment."""
        settings = Settings(database_url="postgresql://main:pass@localhost/main")
        assert settings.get_database_url() == "postgresql://main:pass@localhost/main"

    def test_get_database_url_test(self):
        """Test get_database_url for test environment."""
        settings = Settings(
            database_url="postgresql://main:pass@localhost/main",
            test_database_url="postgresql://test:pass@localhost/test",
        )

        assert (
            settings.get_database_url(test=False)
            == "postgresql://main:pass@localhost/main"
        )
        assert (
            settings.get_database_url(test=True)
            == "postgresql://test:pass@localhost/test"
        )

    def test_get_database_url_test_fallback(self):
        """Test get_database_url fallback when test_database_url is None."""
        settings = Settings(
            database_url="postgresql://main:pass@localhost/main", test_database_url=None
        )

        assert (
            settings.get_database_url(test=True)
            == "postgresql://main:pass@localhost/main"
        )

    def test_game_configuration_defaults(self):
        """Test game configuration defaults."""
        settings = Settings()

        assert settings.max_hints_per_quest == 3
        assert settings.default_quest_time_limit == 300
        assert settings.streak_reset_hours == 48
        assert settings.leaderboard_size == 100

    def test_optional_fields_defaults(self):
        """Test optional fields have correct defaults."""
        settings = Settings()

        assert settings.telegram_webhook_url is None
        assert settings.mini_app_url is None
        assert settings.sentry_dsn is None
        assert settings.test_database_url is None

    @pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR"])
    def test_valid_log_levels(self, log_level):
        """Test valid log levels."""
        settings = Settings(log_level=log_level)
        assert settings.log_level == log_level

    def test_cors_origins_default(self):
        """Test default CORS origins."""
        settings = Settings()
        expected_origins = [
            "http://localhost:3000",
            "https://your-frontend-domain.com",
        ]
        assert settings.allowed_origins == expected_origins
