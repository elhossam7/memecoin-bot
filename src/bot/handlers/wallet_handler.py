from telegram import Update
from telegram.ext import ContextTypes

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /wallet command"""
    await update.message.reply_text("Wallet functionality coming soon!")
