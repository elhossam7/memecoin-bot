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
from .handlers import trade_handler as trade, wallet_handler as wallet, portfolio 

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
        from .menus.dashboard import start_command, menu_callback
        from .menus.settings import show_settings
        from .handlers.settings_commands import set_slippage, toggle_mev, set_tip
        
        # Commands
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("settings", show_settings))
        self.application.add_handler(CommandHandler("set_slippage", set_slippage))
        self.application.add_handler(CommandHandler("toggle_mev", toggle_mev))
        self.application.add_handler(CommandHandler("set_tip", set_tip))
        self.application.add_handler(CommandHandler("trade", trade.handle_trade))
        self.application.add_handler(CommandHandler("wallet", wallet.handle_wallet))
        self.application.add_handler(CommandHandler("portfolio", portfolio.handle_portfolio))
        
        # Callbacks
        self.application.add_handler(CallbackQueryHandler(menu_callback))

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