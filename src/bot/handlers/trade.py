from telegram import Update
from telegram.ext import ContextTypes

async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if not args:
            await update.message.reply_text(
                "🔄 Trading Options:\n"
                "/trade buy <token> <amount>\n"
                "/trade sell <token> <amount>\n"
                "/trade limit <token> <price> <amount>"
            )
            return

        action = args[0].lower()
        if action == "buy":
            await handle_buy(update, context, args[1:])
        elif action == "sell":
            await handle_sell(update, context, args[1:])
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
