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
            'show_tokens': True,
            'gas_limit': 500000,
            'priority_gas': False,
            'max_gas': 100,
            'auto_approve': False,
            'max_buy_tax': 10,
            'sell_multiplier': 1.5,
            'default_buy_amount': 0.1,
            'auto_sells': True
        }
        
        # Create a multi-page menu system
        self.keyboard = [
            # Page 1: Basic Settings
            [InlineKeyboardButton("💰 Wallet ($%.2f)" % self.settings_data['wallet_balance'], 
                                callback_data='settings_balance')],
            [InlineKeyboardButton("🚀 Turbo Slippage (%d%%)" % self.settings_data['turbo_slippage'], 
                                callback_data='settings_turbo')],
            [InlineKeyboardButton("🛡️ Anti-MEV: %s" % ('✅' if self.settings_data['anti_mev'] else '❌'), 
                                callback_data='settings_mev')],
            # Page 2: Trading Settings
            [InlineKeyboardButton("💎 Buy Tip: %.1f%%" % self.settings_data['buy_tip'], 
                                callback_data='settings_buy_tip'),
             InlineKeyboardButton("💎 Sell Tip: %.1f%%" % self.settings_data['sell_tip'], 
                                callback_data='settings_sell_tip')],
            [InlineKeyboardButton("⛽ Gas: %d" % self.settings_data['gas_limit'], 
                                callback_data='settings_gas'),
             InlineKeyboardButton("🔥 Priority: %s" % ('✅' if self.settings_data['priority_gas'] else '❌'), 
                                callback_data='settings_priority')],
            # Page 3: Auto Trading
            [InlineKeyboardButton("🤖 Auto Buy: %s" % ('✅' if self.settings_data['auto_buy'] else '❌'), 
                                callback_data='settings_auto_buy'),
             InlineKeyboardButton("🤖 Auto Sell: %s" % ('✅' if self.settings_data['auto_sell'] else '❌'), 
                                callback_data='settings_auto_sell')],
            [InlineKeyboardButton("📈 Buy Amount: %.3f" % self.settings_data['default_buy_amount'], 
                                callback_data='settings_buy_amount'),
             InlineKeyboardButton("📉 Sell Multi: %.1fx" % self.settings_data['sell_multiplier'], 
                                callback_data='settings_sell_multi')],
            # Navigation
            [InlineKeyboardButton("◀️ Back", callback_data='back_to_main'),
             InlineKeyboardButton("More ▶️", callback_data='settings_page_2')]
        ]
        self.markup = InlineKeyboardMarkup(self.keyboard)

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'settings_data' not in context.bot_data:
        context.bot_data['settings_data'] = {
            'wallet_balance': 0.0,
            'turbo_slippage': 1.0,
            'anti_mev': True,
            'buy_tip': 0.1,
            'sell_tip': 0.1,
            'auto_buy': True,
            'auto_sell': True,
            'custom_buy': 0.0,
            'custom_sell': 0.0,
            'show_tokens': True,
            'gas_limit': 500000,
            'priority_gas': False,
            'max_gas': 100,
            'auto_approve': False,
            'max_buy_tax': 10,
            'sell_multiplier': 1.5,
            'default_buy_amount': 0.1,
            'auto_sells': True
        }
    
    menu = SettingsMenu(context.bot_data['settings_data'])
    message = (
        "⚙️ Trading Settings\n\n"
        f"💰 Balance: ${menu.settings_data['wallet_balance']:,.2f}\n"
        f"🚀 Turbo Slippage: {menu.settings_data['turbo_slippage']}%\n"
        f"🛡️ Anti-MEV: {'Enabled' if menu.settings_data['anti_mev'] else 'Disabled'}\n"
        f"⛽ Gas Limit: {menu.settings_data['gas_limit']:,}\n"
        f"🔥 Priority Gas: {'Enabled' if menu.settings_data['priority_gas'] else 'Disabled'}\n"
        f"💎 Tips: Buy {menu.settings_data['buy_tip']}% / Sell {menu.settings_data['sell_tip']}%\n"
        f"🤖 Auto: Buy {'✅' if menu.settings_data['auto_buy'] else '❌'} / "
        f"Sell {'✅' if menu.settings_data['auto_sell'] else '❌'}\n\n"
        "Click buttons below to modify settings:"
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(message, reply_markup=menu.markup)
    else:
        await update.message.reply_text(message, reply_markup=menu.markup)

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if 'settings_data' not in context.bot_data:
        context.bot_data['settings_data'] = {}
    
    settings = context.bot_data['settings_data']
    
    messages = {
        'settings_balance': (
            f"💰 Wallet Balance: ${settings.get('wallet_balance', 0):,.2f}\n\n"
            "To deposit funds, use:\n"
            "/deposit <amount> <currency>\n\n"
            "Example:\n"
            "/deposit 0.1 ETH\n"
            "/deposit 100 USDT\n\n"
            "⚠️ Make sure to use the correct network!"
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
    if 'settings_data' not in context.bot_data:
        context.bot_data['settings_data'] = {}
    context.bot_data['settings_data'][setting] = value
    return True

async def handle_settings_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    page = int(query.data.split('_')[-1])
    menu = SettingsMenu(context.bot_data.settings_data)
    
    if page == 2:
        # Show advanced settings page
        message = (
            "🔧 Advanced Settings\n\n"
            f"⛽ Max Gas: {menu.settings_data['max_gas']} GWEI\n"
            f"📊 Max Buy Tax: {menu.settings_data['max_buy_tax']}%\n"
            f"📈 Buy Amount: {menu.settings_data['default_buy_amount']} ETH\n"
            f"📉 Sell Multiplier: {menu.settings_data['sell_multiplier']}x"
        )
    else:
        # Show main settings page
        await show_settings(update, context)
        return

    await query.edit_message_text(message, reply_markup=menu.markup)
