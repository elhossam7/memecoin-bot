from telegram import Update
from telegram.ext import CallbackContext
from .commands import handle_trade_command, handle_portfolio_command

def handle_message(update: Update, context: CallbackContext):
    """Handle incoming messages and route them to the appropriate command."""
    text = update.message.text.lower()

    if text.startswith('/trade'):
        handle_trade_command(update, context)
    elif text.startswith('/portfolio'):
        handle_portfolio_command(update, context)
    else:
        update.message.reply_text("Sorry, I didn't understand that command.")