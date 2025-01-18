from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Dict, Any

class SettingsMenu:
    def __init__(self, settings_data: Dict[str, Any] = None):
        self.settings_data = settings_data or {
            'wallet_balance': 0.0,
            'turbo_slippage': 1.0,
            'anti_mev': True,
            'buy_tip': 0.1,
            'sell_tip': 0.1,
            'auto_buy': True,
            'auto_sell': True,
            'custom_buy': 0.0,
            'custom_sell': 0.0,
            'show_tokens': True
        }
        
        self.keyboard = [
            [InlineKeyboardButton("💰 Wallet Balance", callback_data='settings_balance'),
             InlineKeyboardButton("🚀 Turbo Slippage", callback_data='settings_turbo')],
            [InlineKeyboardButton("🛡️ Anti-MEV", callback_data='settings_mev'),
             InlineKeyboardButton("💎 Trade Tips", callback_data='settings_tips')],
            [InlineKeyboardButton("🤖 Auto Trading", callback_data='settings_auto'),
             InlineKeyboardButton("📊 Custom Prices", callback_data='settings_custom')],
            [InlineKeyboardButton("👁️ Token Visibility", callback_data='settings_visibility'),
             InlineKeyboardButton("🔙 Back", callback_data='back_to_main')]
        ]
        self.markup = InlineKeyboardMarkup(self.keyboard)

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = SettingsMenu(getattr(context.bot_data, 'settings_data', None))
    message = (
        "⚙️ Trading Settings\n\n"
        "Configure your trading parameters:"
    )
    if update.callback_query:
        await update.callback_query.edit_message_text(message, reply_markup=menu.markup)
    else:
        await update.message.reply_text(message, reply_markup=menu.markup)

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not hasattr(context.bot_data, 'settings_data'):
        context.bot_data.settings_data = {}
    
    settings = context.bot_data.settings_data
    
    messages = {
        'settings_balance': (
            f"💰 Wallet Balance: ${settings.get('wallet_balance', 0):,.2f}\n\n"
            "To deposit funds, use:\n/deposit <amount> <currency>"
        ),
        'settings_turbo': (
            f"🚀 Turbo Slippage: {settings.get('turbo_slippage', 1)}%\n\n"
            "Adjust with:\n/set_slippage <percentage>"
        ),
        'settings_mev': (
            f"🛡️ Anti-MEV Protection: {'Enabled' if settings.get('anti_mev', True) else 'Disabled'}\n\n"
            "Toggle with:\n/toggle_mev"
        ),
        'settings_tips': (
            f"💎 Buy Tip: {settings.get('buy_tip', 0.1)}%\n"
            f"💎 Sell Tip: {settings.get('sell_tip', 0.1)}%\n\n"
            "Modify with:\n/set_tip buy/sell <percentage>"
        ),
        'settings_auto': (
            f"🤖 Auto Buy: {'Enabled' if settings.get('auto_buy', True) else 'Disabled'}\n"
            f"🤖 Auto Sell: {'Enabled' if settings.get('auto_sell', True) else 'Disabled'}\n\n"
            "Toggle with:\n/auto buy/sell on/off"
        ),
        'settings_custom': (
            f"📊 Custom Buy: ${settings.get('custom_buy', 0):,.2f}\n"
            f"📊 Custom Sell: ${settings.get('custom_sell', 0):,.2f}\n\n"
            "Set with:\n/custom_price buy/sell <amount>"
        ),
        'settings_visibility': (
            f"👁️ Tokens are currently: {'Visible' if settings.get('show_tokens', True) else 'Hidden'}\n\n"
            "Toggle with:\n/toggle_tokens"
        )
    }
    
    if query.data in messages:
        menu = SettingsMenu(settings)
        await query.edit_message_text(
            text=messages[query.data],
            reply_markup=menu.markup
        )

async def update_setting(context: ContextTypes.DEFAULT_TYPE, setting: str, value: Any) -> bool:
    """Helper function to update settings safely"""
    if not hasattr(context.bot_data, 'settings_data'):
        context.bot_data.settings_data = {}
    context.bot_data.settings_data[setting] = value
    return True
