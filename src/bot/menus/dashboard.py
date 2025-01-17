
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💰 Trade", callback_data="menu_trade"),
            InlineKeyboardButton("👛 Wallet", callback_data="menu_wallet")
        ],
        [
            InlineKeyboardButton("📊 Portfolio", callback_data="menu_portfolio"),
            InlineKeyboardButton("⚡ Quick Snipe", callback_data="menu_snipe")
        ],
        [
            InlineKeyboardButton("📈 Copy Trade", callback_data="menu_copy"),
            InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
        ]
    ]
    
    welcome_text = (
        "🤖 *Welcome to MemeCoin Trading Bot*\n\n"
        "Select an option to get started:"
    )
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        welcome_text, 
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )