from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

class DashboardMenu:
    def __init__(self):
        self.keyboard = [
            [InlineKeyboardButton("🔄 Trade", callback_data='trade'),
             InlineKeyboardButton("👛 Wallet", callback_data='wallet')],
            [InlineKeyboardButton("📊 Portfolio", callback_data='portfolio'),
             InlineKeyboardButton("⚙️ Settings", callback_data='settings')]
        ]
        self.markup = InlineKeyboardMarkup(self.keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = DashboardMenu()
    await update.message.reply_text(
        "Welcome to MemeCoin Trading Bot! 🚀\nPlease select an option:",
        reply_markup=menu.markup
    )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'trade':
        await query.message.edit_text("Trading menu coming soon!")
    elif query.data == 'wallet':
        await query.message.edit_text("Wallet info coming soon!")
    elif query.data == 'portfolio':
        await query.message.edit_text("Portfolio details coming soon!")
    elif query.data == 'settings':
        from .settings import show_settings
        await show_settings(update, context)
    elif query.data.startswith('settings_'):
        from .settings import handle_settings_callback
        await handle_settings_callback(update, context)
    elif query.data == 'back_to_main':
        menu = DashboardMenu()
        await query.message.edit_text(
            "Welcome to MemeCoin Trading Bot! 🚀\nPlease select an option:",
            reply_markup=menu.markup
        )