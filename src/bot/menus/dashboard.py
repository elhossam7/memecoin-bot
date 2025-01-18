from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

class DashboardMenu:
    def __init__(self):
        self.keyboard = [
            ['📈 Price', '💰 Buy/Sell'],
            ['📊 Chart', '📢 News'],
            ['ℹ️ Info', '⚙️ Settings']
        ]

    async def display(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_markup = ReplyKeyboardMarkup(self.keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Welcome to Memecoin Bot! Choose an option:",
            reply_markup=reply_markup
        )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dashboard = DashboardMenu()
    await dashboard.display(update, context)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    responses = {
        '📈 Price': 'Current price information...',
        '💰 Buy/Sell': 'Trading information...',
        '📊 Chart': 'Chart information...',
        '📢 News': 'Latest news...',
        'ℹ️ Info': 'Bot information...',
        '⚙️ Settings': 'Settings options...'
    }
    response = responses.get(text, 'Please use the menu options.')
    await update.message.reply_text(response)
