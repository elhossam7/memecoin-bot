from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - display main menu."""
    keyboard = [
        [
            InlineKeyboardButton("Trade", callback_data='trade'),
            InlineKeyboardButton("Wallet", callback_data='wallet')
        ],
        [InlineKeyboardButton("Portfolio", callback_data='portfolio')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Welcome to MemeBot! Please select an option:',
        reply_markup=reply_markup
    )

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'trade':
        await query.message.edit_text("Trading functionality coming soon!")
    elif query.data == 'wallet':
        await query.message.edit_text("Wallet functionality coming soon!")
    elif query.data == 'portfolio':
        await query.message.edit_text("Portfolio functionality coming soon!")