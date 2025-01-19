import asyncio
import re
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
from telegram.error import InvalidToken

from .wallet_manager import WalletManager
from .menus.settings import SettingsMenu, show_settings, handle_settings_callback

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
        self.app = Application.builder().token(token).build()
        self._setup_handlers()
        self.settings_data = {
            'wallet_balance': 0.0,
            'turbo_slippage': 1.0,
            'anti_mev': True,
            'gas_limit': 500000,
            'priority_gas': False,
            'auto_buy': True,
            'auto_sell': True
        }
        self.wallet_manager = WalletManager()

    @staticmethod
    def _is_valid_token(token: str) -> bool:
        """Validate Telegram bot token format."""
        if not isinstance(token, str):
            return False
        # More lenient regex that matches the Telegram bot token format
        return bool(re.match(r'^\d+:[A-Za-z0-9_-]+$', token.strip()))

    def _setup_handlers(self):
        # Add command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        # Add callback query handler for settings
        self.app.add_handler(CallbackQueryHandler(handle_settings_callback))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        # Check if user has a wallet
        wallet = self.wallet_manager.get_wallet(user_id)
        if not wallet:
            # Create new wallet
            wallet_result = self.wallet_manager.create_wallet(user_id)
            if wallet_result['success']:
                # Escape special characters for MarkdownV2
                address = wallet_result['address'].replace('-', '\\-').replace('.', '\\.')
                welcome_text = (
                    "🎉 Welcome\\! I've created a new wallet for you:\n\n"
                    f"Address: `{address}`\n\n"
                    "⚠️ Please store this address safely\\!"
                )
                await update.message.reply_text(
                    welcome_text,
                    parse_mode='MarkdownV2'
                )
            else:
                await update.message.reply_text(
                    "❌ Sorry, there was an error creating your wallet\\. Please try again later\\."
                )
                return

        # Show main menu
        keyboard = [
            ['🛒 Buy', '💰 Sell', '📊 Positions'],
            ['📈 Limit Orders', '⏱️ DCA Orders'],
            ['👥 Copy Trade', '🎯 Sniper', '⚔️ Trenches'],
            ['👀 Watchlist', '💳 Withdraw'],
            ['⚙️ Settings', '❓ Help', '🔄 Refresh'],
            ['🤝 Referrals', '📱 Social']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        # Escape special characters for MarkdownV2
        address = wallet['address'].replace('-', '\\-').replace('.', '\\.')
        balance = str(wallet['balance']).replace('.', '\\.')
        
        # Include wallet info in welcome message
        welcome_msg = (
            "Welcome to Memecoin Trading Bot\\!\n\n"
            "💼 Your Wallet:\n"
            f"Address: `{address}`\n"
            f"Balance: {balance} ETH\n\n"
            "Choose an option from the menu below:"
        )
        
        try:
            await update.message.reply_text(
                welcome_msg,
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
        except Exception as e:
            logger.error(f"Error sending welcome message: {e}")
            # Fallback to plain text if markdown fails
            await update.message.reply_text(
                welcome_msg.replace('\\', ''),
                reply_markup=reply_markup
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text

        if text == '⚙️ Settings':
            await show_settings(update, context)
            return

        responses = {
            '🛒 Buy': "Buy Order Menu\nEnter token address or select from trending",
            '💰 Sell': "Sell Order Menu\nSelect token from your portfolio",
            '📊 Positions': "Current Active Positions:\nNo open positions",
            '📈 Limit Orders': "Limit Orders:\nNo active limit orders",
            '⏱️ DCA Orders': "DCA (Dollar Cost Average) Orders:\nNo active DCA orders",
            '👥 Copy Trade': "Copy Trading Menu\nSelect traders to copy",
            '🎯 Sniper': "Token Sniper Settings\nSet up your snipe parameters",
            '⚔️ Trenches': "Trenches Trading Mode\nSet up your trading trenches",
            '👀 Watchlist': "Your Watchlist\nNo tokens added",
            '💳 Withdraw': f"Wallet Balance: ${self.settings_data['wallet_balance']:,.2f}\nEnter amount to withdraw",
            '⚙️ Settings': self._get_settings_text(),
            '❓ Help': "Trading Bot Help Menu\n/buy - Place buy order\n/sell - Place sell order\n/limits - Set limit orders",
            '🔄 Refresh': "Refreshing market data...\nDone ✅",
            '🤝 Referrals': "Your Referral Link: t.me/yourbot?start=ref123\nReferral Rewards: $0.00",
            '📱 Social': "Join our community:\nTelegram: t.me/tradingbot\nTwitter: @tradingbot"
        }

        response = responses.get(text, 'Please use the menu options.')
        await update.message.reply_text(response)

    def _get_settings_text(self):
        return (
            "⚙️ Current Settings:\n"
            f"Anti-MEV: {'✅' if self.settings_data['anti_mev'] else '❌'}\n"
            f"Auto Buy: {'✅' if self.settings_data['auto_buy'] else '❌'}\n"
            f"Auto Sell: {'✅' if self.settings_data['auto_sell'] else '❌'}\n"
            f"Gas Limit: {self.settings_data['gas_limit']}\n"
            f"Slippage: {self.settings_data['turbo_slippage']}%"
        )

    def run(self):
        print("Bot is starting...")
        self.app.run_polling()