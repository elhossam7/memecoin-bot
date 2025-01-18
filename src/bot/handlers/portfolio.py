from telegram import Update
from telegram.ext import ContextTypes

async def handle_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /portfolio command"""
    await update.message.reply_text("Portfolio functionality coming soon!")
