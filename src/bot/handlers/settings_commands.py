from telegram import Update
from telegram.ext import ContextTypes
from ..menus.settings import update_setting, SettingsMenu

async def set_slippage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if 0 <= value <= 100:
            await update_setting(context, 'turbo_slippage', value)
            await update.message.reply_text(f"✅ Turbo Slippage set to {value}%")
        else:
            await update.message.reply_text("❌ Slippage must be between 0 and 100%")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_slippage <percentage>")

async def toggle_mev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('anti_mev', True)
    await update_setting(context, 'anti_mev', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Anti-MEV protection {status}")

async def set_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tip_type, value = context.args
        value = float(value)
        if tip_type not in ['buy', 'sell']:
            raise ValueError("Type must be 'buy' or 'sell'")
        if 0 <= value <= 5:  # Maximum 5% tip
            setting_key = f'{tip_type}_tip'
            await update_setting(context, setting_key, value)
            await update.message.reply_text(f"✅ {tip_type.title()} tip set to {value}%")
        else:
            await update.message.reply_text("❌ Tip must be between 0 and 5%")
    except (IndexError, ValueError) as e:
        await update.message.reply_text("❌ Usage: /set_tip buy/sell <percentage>")

# Add more command handlers for other settings...
