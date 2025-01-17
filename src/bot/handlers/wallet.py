
from telegram import Update
from telegram.ext import ContextTypes

async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            wallet_address = context.user_data.get('wallet_address', 'Not connected')
            balance = await get_wallet_balance(wallet_address)
            
            await update.message.reply_text(
                f"👛 *Wallet Info*\n\n"
                f"Address: `{wallet_address}`\n"
                f"Balance: {balance}\n\n"
                "Commands:\n"
                "/wallet connect <address>\n"
                "/wallet disconnect\n"
                "/wallet transfer <to> <amount>",
                parse_mode="Markdown"
            )
            return

        action = context.args[0].lower()
        if action == "connect":
            await connect_wallet(update, context)
        elif action == "disconnect":
            await disconnect_wallet(update, context)
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")