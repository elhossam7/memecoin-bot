from telegram import Update
from telegram.ext import ContextTypes

async def handle_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /trade command"""
    await update.message.reply_text("Trading functionality coming soon!")
