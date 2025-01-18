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
from .menus.dashboard import menu_callback  # Add this import

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
        
        # Initialize settings data
        self.application.bot_data['settings_data'] = {
            'wallet_balance': 0.0,
            'turbo_slippage': 1.0,
            'anti_mev': True,
            'buy_tip': 0.1,
            'sell_tip': 0.1,
            'auto_buy': True,
            'auto_sell': True,
            'custom_buy': 0.0,
            'custom_sell': 0.0,
            'show_tokens': True,
            'gas_limit': 500000,
            'priority_gas': False,
            'max_gas': 100,
            'auto_approve': False,
            'max_buy_tax': 10,
            'sell_multiplier': 1.5,
            'default_buy_amount': 0.1,
            'auto_sells': True
        }
        
        self._register_handlers()

    @staticmethod
    def _is_valid_token(token: str) -> bool:
        """Validate Telegram bot token format."""
        if not isinstance(token, str):
            return False
        # Simpler regex that just checks for number:string format
        return bool(re.match(r'^\d+:[A-Za-z0-9_-]+$', token))

    def _register_handlers(self):
        from .menus.main_menu import show_main_menu, handle_main_menu_callback
        from .menus.settings import show_settings, handle_settings_page
        from .handlers.settings_commands import (
            set_slippage, toggle_mev, set_tip, handle_deposit
        )
        
        # Commands
        self.application.add_handler(CommandHandler("start", show_main_menu))  # Changed to main menu
        self.application.add_handler(CommandHandler("menu", show_main_menu))
        self.application.add_handler(CommandHandler("settings", show_settings))
        self.application.add_handler(CommandHandler("set_slippage", set_slippage))
        self.application.add_handler(CommandHandler("toggle_mev", toggle_mev))
        self.application.add_handler(CommandHandler("set_tip", set_tip))
        self.application.add_handler(CommandHandler("trade", trade.handle_trade))
        self.application.add_handler(CommandHandler("wallet", wallet.handle_wallet))
        self.application.add_handler(CommandHandler("portfolio", portfolio.handle_portfolio))
        self.application.add_handler(CommandHandler("deposit", handle_deposit))
        
        # Callbacks
        self.application.add_handler(CallbackQueryHandler(handle_main_menu_callback))
        self.application.add_handler(CallbackQueryHandler(menu_callback))  # This should now work
        self.application.add_handler(
            CallbackQueryHandler(
                handle_settings_page, 
                pattern='^settings_page_[0-9]+$'
            )
        )

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