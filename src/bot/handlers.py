from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ContextTypes

async def handle_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle trade command"""
    await update.message.reply_text("Trading functionality coming soon!")

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet command"""
    await update.message.reply_text("Wallet functionality coming soon!")

async def handle_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle portfolio command"""
    await update.message.reply_text("Portfolio functionality coming soon!")

# Export handlers
trade_handler = handle_trade
wallet_handler = handle_wallet
portfolio_handler = handle_portfolio

def register_handlers(application):
    application.add_handler(CommandHandler("trade", handle_trade))
    application.add_handler(CommandHandler("portfolio", handle_portfolio))

def handle_message(update: Update, context: CallbackContext):
    """Handle incoming messages and route them to the appropriate command."""
    text = update.message.text.lower()

    if text.startswith('/trade'):
        handle_trade(update, context)
    elif text.startswith('/portfolio'):
        handle_portfolio(update, context)
    else:
        update.message.reply_text("Sorry, I didn't understand that command.")