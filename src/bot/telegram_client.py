import asyncio
import re
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
from telegram.error import InvalidToken
from .handlers import trade, wallet, portfolio 
from .menus import dashboard

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str):
        logger.debug(f"Initializing TelegramBot with token length: {len(token) if token else 0}")
        if not token:
            raise InvalidToken("Telegram bot token is missing")
        
        # Less strict token validation
        if not self._is_valid_token(token):
            logger.error(f"Invalid token format. Token should be in format: NUMBER:ALPHANUMERIC")
            raise InvalidToken("Invalid Telegram bot token format")
        
        self.token = token
        self.application = Application.builder().token(token).build()
        self._register_handlers()

    @staticmethod
    def _is_valid_token(token: str) -> bool:
        """Validate Telegram bot token format."""
        if not isinstance(token, str):
            return False
        # Simpler regex that just checks for number:string format
        return bool(re.match(r'^\d+:[A-Za-z0-9_-]+$', token))

    def _register_handlers(self):
        # Commands
        self.application.add_handler(CommandHandler("start", dashboard.start_command))
        self.application.add_handler(CommandHandler("trade", trade.trade_command))
        self.application.add_handler(CommandHandler("wallet", wallet.wallet_command))
        self.application.add_handler(CommandHandler("portfolio", portfolio.portfolio_command))
        
        # Callbacks
        self.application.add_handler(CallbackQueryHandler(dashboard.menu_callback))

    async def start(self):
        """Start the bot asynchronously."""
        try:
            await self.application.initialize()
            await self.application.start()
            # Use simple polling without signal handlers
            await self.application.updater.start_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"Error in bot startup: {e}")
            await self.stop()
            raise

    async def stop(self):
        """Stop the bot asynchronously."""
        try:
            if hasattr(self, 'application') and self.application.running:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            raise