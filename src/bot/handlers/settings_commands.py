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
async def toggle_turbo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('turbo_enabled', False)
    await update_setting(context, 'turbo_enabled', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Turbo mode {status}")

async def set_gas_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(context.args[0])
        if value > 0:
            await update_setting(context, 'gas_limit', value)
            await update.message.reply_text(f"✅ Gas limit set to {value}")
        else:
            await update.message.reply_text("❌ Gas limit must be greater than 0")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_gas_limit <value>")

async def toggle_auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('auto_approve', False)
    await update_setting(context, 'auto_approve', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Auto token approval {status}")
# Add more command handlers for other settings...
async def toggle_priority_gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('priority_gas', False)
    await update_setting(context, 'priority_gas', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Priority gas {status}")

async def set_max_gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if value > 0:
            await update_setting(context, 'max_gas', value)
            await update.message.reply_text(f"✅ Max gas price set to {value} GWEI")
        else:
            await update.message.reply_text("❌ Max gas price must be greater than 0")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_max_gas <gwei>")

async def toggle_auto_sells(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('auto_sells', False)
    await update_setting(context, 'auto_sells', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Auto sells {status}")

async def set_sell_multiplier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if value >= 1:
            await update_setting(context, 'sell_multiplier', value)
            await update.message.reply_text(f"✅ Sell multiplier set to {value}x")
        else:
            await update.message.reply_text("❌ Sell multiplier must be >= 1")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_sell_multiplier <value>")

async def set_buy_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if value > 0:
            await update_setting(context, 'default_buy_amount', value)
            await update.message.reply_text(f"✅ Default buy amount set to {value} ETH")
        else:
            await update.message.reply_text("❌ Buy amount must be greater than 0")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_buy_amount <eth>")

async def toggle_auto_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = context.bot_data.settings_data.get('auto_buy', False)
    await update_setting(context, 'auto_buy', not current)
    status = "enabled" if not current else "disabled"
    await update.message.reply_text(f"✅ Auto buy {status}")

async def set_max_buy_tax(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        if 0 <= value <= 100:
            await update_setting(context, 'max_buy_tax', value)
            await update.message.reply_text(f"✅ Max buy tax set to {value}%")
        else:
            await update.message.reply_text("❌ Max buy tax must be between 0 and 100%")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Usage: /set_max_buy_tax <percentage>")

async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle deposit command with amount and currency"""
    try:
        if len(context.args) != 2:
            raise ValueError("Usage: /deposit <amount> <currency>\nExample: /deposit 0.1 ETH")

        amount = float(context.args[0])
        currency = context.args[1].upper()
        
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        # Get current balance
        current_balance = context.bot_data['settings_data'].get('wallet_balance', 0.0)
        
        # Update wallet balance
        new_balance = current_balance + amount
        await update_setting(context, 'wallet_balance', new_balance)

        # Generate deposit address (this should integrate with your actual wallet system)
        deposit_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Example address
        
        success_message = (
            f"✅ Deposit request processed:\n\n"
            f"Amount: {amount} {currency}\n"
            f"New Balance: ${new_balance:,.2f}\n\n"
            f"Please send your {currency} to:\n`{deposit_address}`\n\n"
            "⚠️ Only send tokens on the correct network!"
        )
        
        await update.message.reply_text(success_message)
        
    except ValueError as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    except Exception as e:
        await update.message.reply_text("❌ An error occurred while processing your deposit.")
        logger.error(f"Deposit error: {str(e)}")