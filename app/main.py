"""Main application entry point for VimMaster."""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from app.config.settings import settings
from app.config.database import init_database, close_database
from app.bot.handlers import start, menu

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher (will be created when needed)
bot = None
dp = Dispatcher()


def get_bot() -> Bot:
    """Get bot instance, creating it if needed."""
    global bot
    if bot is None:
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        
        bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    return bot


def setup_bot() -> None:
    """Setup bot with handlers and middlewares."""
    # Register routers
    dp.include_router(start.router)
    dp.include_router(menu.router)
    
    logger.info("Bot handlers registered successfully")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager."""
    # Startup
    logger.info("Starting VimMaster application...")
    
    # Initialize database
    await init_database()
    
    # Setup bot
    setup_bot()
    
    # Start bot polling in background
    if settings.telegram_bot_token:
        bot_task = asyncio.create_task(start_bot_polling())
        logger.info("Bot polling started")
    else:
        logger.warning("No Telegram bot token provided, bot will not start")
        bot_task = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down VimMaster application...")
    
    # Stop bot
    if bot_task and not bot_task.done():
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass
        logger.info("Bot polling stopped")
    
    # Close database connections
    await close_database()
    
    # Close bot session
    current_bot = get_bot()
    await current_bot.session.close()


async def start_bot_polling() -> None:
    """Start bot polling."""
    try:
        current_bot = get_bot()
        await dp.start_polling(current_bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Bot polling failed: {e}")
        raise


# FastAPI app
app = FastAPI(
    title="VimMaster API",
    description="Educational Telegram game for learning Vim commands",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": "VimMaster",
        "version": "0.1.0",
        "description": "Educational Telegram game for learning Vim commands",
        "status": "running",
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual database health check
        "bot": "running" if settings.telegram_bot_token else "not configured",
    }


async def main() -> None:
    """Main function for running bot only (without FastAPI)."""
    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set!")
        sys.exit(1)
    
    logger.info("Starting VimMaster bot...")
    
    # Initialize database
    await init_database()
    
    # Setup bot
    setup_bot()
    
    try:
        # Start polling
        current_bot = get_bot()
        await dp.start_polling(current_bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot failed: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        await close_database()
        if bot:
            await bot.session.close()


if __name__ == "__main__":
    # Run bot only (without FastAPI)
    asyncio.run(main())