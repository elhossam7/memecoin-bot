from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - display main menu."""
    keyboard = [
        [
            InlineKeyboardButton("💱 Buy/Sell", callback_data='trade'),
            InlineKeyboardButton("📊 Limit Orders", callback_data='limit_orders')
        ],
        [
            InlineKeyboardButton("💎 Assets", callback_data='assets'),
            InlineKeyboardButton("👛 Wallet", callback_data='wallet')
        ],
        [
            InlineKeyboardButton("🔄 New LP", callback_data='new_lp'),
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ],
        [InlineKeyboardButton("🌐 Language", callback_data='language')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '🤖 Welcome to MemeBot! Please select an option:',
        reply_markup=reply_markup
    )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'settings':
        from .settings import settings_menu
        await settings_menu(update, context)
        return

    responses = {
        'trade': "💱 Trading functionality coming soon!",
        'limit_orders': "📊 Limit Orders functionality coming soon!",
        'assets': "💎 Assets functionality coming soon!",
        'wallet': "👛 Wallet functionality coming soon!",
        'new_lp': "🔄 New LP functionality coming soon!",
        'settings': "⚙️ Settings functionality coming soon!",
        'language': "🌐 Language functionality coming soon!"
    }
    
    if query.data in responses:
        await query.message.edit_text(responses[query.data])