"""Tests for main application module."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app, setup_bot, start_bot_polling


class TestFastAPIApp:
    """Test FastAPI application."""

    def test_app_creation(self):
        """Test FastAPI app is created properly."""
        assert app is not None
        assert app.title == "VimMaster API"
        assert app.description == "Educational Telegram game for learning Vim commands"
        assert app.version == "0.1.0"

    def test_root_endpoint(self):
        """Test root endpoint."""
        with TestClient(app) as client:
            with patch('app.main.init_database', new_callable=AsyncMock):
                with patch('app.main.close_database', new_callable=AsyncMock):
                    with patch('app.main.start_bot_polling', new_callable=AsyncMock):
                        with patch('app.main.settings.telegram_bot_token', ''):
                            response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == "VimMaster"
        assert data["version"] == "0.1.0"
        assert data["description"] == "Educational Telegram game for learning Vim commands"
        assert data["status"] == "running"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        with TestClient(app) as client:
            with patch('app.main.init_database', new_callable=AsyncMock):
                with patch('app.main.close_database', new_callable=AsyncMock):
                    with patch('app.main.start_bot_polling', new_callable=AsyncMock):
                        with patch('app.main.settings.telegram_bot_token', ''):
                            response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "bot" in data


class TestBotSetup:
    """Test bot setup and polling."""

    @patch('app.main.dp')
    @patch('app.main.logger')
    def test_setup_bot(self, mock_logger, mock_dp):
        """Test bot setup function."""
        setup_bot()
        
        # Verify routers are included
        assert mock_dp.include_router.call_count == 2
        mock_logger.info.assert_called_with("Bot handlers registered successfully")

    @pytest.mark.asyncio
    async def test_start_bot_polling_success(self):
        """Test successful bot polling start."""
        with patch('app.main.dp') as mock_dp:
            mock_dp.start_polling = AsyncMock()
            mock_dp.resolve_used_update_types.return_value = ["message", "callback_query"]
            
            await start_bot_polling()
            
            mock_dp.start_polling.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_bot_polling_failure(self):
        """Test bot polling failure handling."""
        with patch('app.main.dp') as mock_dp:
            mock_dp.start_polling = AsyncMock(side_effect=Exception("Polling failed"))
            mock_dp.resolve_used_update_types.return_value = ["message"]
            
            with patch('app.main.logger') as mock_logger:
                with pytest.raises(Exception, match="Polling failed"):
                    await start_bot_polling()
                
                mock_logger.error.assert_called_with("Bot polling failed: Polling failed")


class TestMainFunction:
    """Test main function for bot-only mode."""

    @pytest.mark.asyncio
    async def test_main_no_token(self):
        """Test main function with no bot token."""
        with patch('app.main.settings.telegram_bot_token', ''):
            with patch('app.main.logger') as mock_logger:
                with pytest.raises(SystemExit):
                    await app.main.main()
                
                mock_logger.error.assert_called_with("TELEGRAM_BOT_TOKEN is not set!")

    @pytest.mark.asyncio
    async def test_main_success_flow(self):
        """Test successful main function flow."""
        with patch('app.main.settings.telegram_bot_token', '123456:test_token'):
            with patch('app.main.init_database', new_callable=AsyncMock) as mock_init:
                with patch('app.main.setup_bot') as mock_setup:
                    with patch('app.main.dp') as mock_dp:
                        with patch('app.main.close_database', new_callable=AsyncMock) as mock_close:
                            with patch('app.main.bot.session.close', new_callable=AsyncMock) as mock_bot_close:
                                # Mock polling to raise KeyboardInterrupt for clean exit
                                mock_dp.start_polling = AsyncMock(side_effect=KeyboardInterrupt())
                                mock_dp.resolve_used_update_types.return_value = ["message"]
                                
                                with patch('app.main.logger') as mock_logger:
                                    await app.main.main()
                                
                                mock_init.assert_called_once()
                                mock_setup.assert_called_once()
                                mock_dp.start_polling.assert_called_once()
                                mock_close.assert_called_once()
                                mock_bot_close.assert_called_once()
                                mock_logger.info.assert_any_call("Bot stopped by user")

    @pytest.mark.asyncio
    async def test_main_bot_failure(self):
        """Test main function with bot failure."""
        with patch('app.main.settings.telegram_bot_token', '123456:test_token'):
            with patch('app.main.init_database', new_callable=AsyncMock):
                with patch('app.main.setup_bot'):
                    with patch('app.main.dp') as mock_dp:
                        mock_dp.start_polling = AsyncMock(side_effect=Exception("Bot failed"))
                        mock_dp.resolve_used_update_types.return_value = ["message"]
                        
                        with patch('app.main.logger') as mock_logger:
                            with patch('app.main.close_database', new_callable=AsyncMock):
                                with patch('app.main.bot.session.close', new_callable=AsyncMock):
                                    with pytest.raises(SystemExit):
                                        await app.main.main()
                            
                            mock_logger.error.assert_called_with("Bot failed: Bot failed")