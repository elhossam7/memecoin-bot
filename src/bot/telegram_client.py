import asyncio
import re
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from telegram.error import InvalidToken

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self, token: str):
        logger.debug(f"Initializing TelegramClient with token length: {len(token) if token else 0}")
        if not token:
            raise InvalidToken("Telegram bot token is missing")
        
        # Less strict token validation
        if not self._is_valid_token(token):
            logger.error(f"Invalid token format. Token should be in format: NUMBER:ALPHANUMERIC")
            raise InvalidToken("Invalid Telegram bot token format")
        
        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()

    @staticmethod
    def _is_valid_token(token: str) -> bool:
        """Validate Telegram bot token format."""
        if not isinstance(token, str):
            return False
        # Simpler regex that just checks for number:string format
        return bool(re.match(r'^\d+:[A-Za-z0-9_-]+$', token))

    def _setup_handlers(self):
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("status", self._status_command))
        
        # Add message handler for non-commands
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Welcome to the MemeCoin Trading Bot!\n"
            "Use /help to see available commands."
        )

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/status - Show current trading status"
        )

    async def _status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Trading bot is active and monitoring markets.")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please use commands to interact with the bot.")

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