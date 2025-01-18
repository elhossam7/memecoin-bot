import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import time

# Initialize logger
logger = logging.getLogger(__name__)

class MainMenu:
    def __init__(self, user_data: dict = None):
        self.user_data = user_data or {}
        self.create_keyboard()

    def create_keyboard(self):
        # Trading Buttons (Row 1-2)
        self.keyboard = [
            [
                InlineKeyboardButton("🛒 Buy", callback_data='buy'),
                InlineKeyboardButton("💰 Sell", callback_data='sell'),
                InlineKeyboardButton("📊 Positions", callback_data='positions')
            ],
            [
                InlineKeyboardButton("📈 Limit Orders", callback_data='limits'),
                InlineKeyboardButton("⏱️ DCA Orders", callback_data='dca')
            ],
            # Advanced Trading (Row 3)
            [
                InlineKeyboardButton("👥 Copy Trade", callback_data='copy'),
                InlineKeyboardButton("🎯 Sniper", callback_data='sniper'),
                InlineKeyboardButton("⚔️ Trenches", callback_data='trenches')
            ],
            # Portfolio Management (Row 4)
            [
                InlineKeyboardButton("👀 Watchlist", callback_data='watchlist'),
                InlineKeyboardButton("💳 Withdraw", callback_data='withdraw')
            ],
            # System Buttons (Row 5)
            [
                InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
                InlineKeyboardButton("❓ Help", callback_data='help'),
                InlineKeyboardButton("🔄 Refresh", callback_data='refresh')
            ],
            # Social & Referral (Row 6)
            [
                InlineKeyboardButton("🤝 Referrals", callback_data='referrals'),
                InlineKeyboardButton("📱 Social", callback_data='social')
            ]
        ]
        self.markup = InlineKeyboardMarkup(self.keyboard)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the main menu with wallet info and warnings"""
    if not context.user_data.get('wallet_address'):
        context.user_data['wallet_address'] = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Example
    
    menu = MainMenu(context.user_data)
    
    # Format wallet balance with proper decimals
    balance = context.user_data.get('balance', 0.0)
    
    # Escape special characters and format message properly
    wallet_address = context.user_data['wallet_address']
    header = (
        "*🏦 Main Menu*\n\n"
        f"💼 *Wallet Address:*\n`{wallet_address}`\n\n"
        f"💰 *Balance:* ${balance:,.2f}\n\n"
        "*📱 Social Links:*\n"
        "• Telegram: @trojan\n"
        "• Twitter: @trojan\\_trades\n\n"
        "*🤖 Suggested Bots:*\n"
        "• @TrojanAIO\\_bot\n"
        "• @TrojanSniper\\_bot\n\n"
        "*⚠️ WARNINGS:*\n"
        "• Beware of Telegram ads\n"
        "• Never click unknown login pages\n"
        "• Avoid fake airdrops\n"
        "• Verify all transactions\n\n"
        f"Last updated: {time.strftime('%H:%M:%S')}"
    )
    
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=header,
                reply_markup=menu.markup,
                parse_mode='MarkdownV2'  # Use MarkdownV2 for better escape handling
            )
        else:
            await update.message.reply_text(
                text=header,
                reply_markup=menu.markup,
                parse_mode='MarkdownV2'  # Use MarkdownV2 for better escape handling
            )
    except Exception as e:
        # Fallback to plain text if markdown parsing fails
        logger.error(f"Error sending menu: {e}")
        plain_text = header.replace('*', '').replace('`', '')
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=plain_text,
                reply_markup=menu.markup
            )
        else:
            await update.message.reply_text(
                text=plain_text,
                reply_markup=menu.markup
            )

async def handle_main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu button callbacks"""
    query = update.callback_query
    await query.answer()
    
    action_messages = {
        'buy': "🛒 Buy cryptocurrencies at market or limit price",
        'sell': "💰 Sell your crypto holdings",
        'positions': "📊 View your open trading positions",
        'limits': "📈 Set up limit orders to buy/sell at specific prices",
        'dca': "⏱️ Configure Dollar-Cost Averaging orders",
        'copy': "👥 Copy successful traders' positions",
        'sniper': "🎯 Quick-buy new tokens with custom gas",
        'trenches': "⚔️ Set up defensive trading positions",
        'watchlist': "👀 Monitor your favorite tokens",
        'withdraw': "💳 Withdraw your funds securely",
        'referrals': "🤝 Share your referral link and earn rewards",
        'social': "📱 Join our community channels",
        'help': "❓ Get help and trading guides",
        'refresh': "refresh"
    }
    
    if query.data in action_messages:
        if query.data == 'refresh':
            await show_main_menu(update, context)
        elif query.data == 'settings':
            from .settings import show_settings
            await show_settings(update, context)
        else:
            await query.edit_message_text(
                f"{action_messages[query.data]}\n\nFeature coming soon!",
                reply_markup=MainMenu(context.user_data).markup
            )
