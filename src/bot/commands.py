from telegram import Update
from telegram.ext import CallbackContext
from .bot import bot  # Ensure bot is imported from the bot.py file

def start(update, context):
    """Start command handler."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the MemeCoin Trading Bot! Use /help to see available commands.")

def help_command(update, context):
    """Help command handler."""
    help_text = (
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/trade - Execute a trade\n"
        "/portfolio - Show your portfolio\n"
        "/alerts - Manage your alerts\n"
        "/status - Check the bot status"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def trade(update, context):
    """Trade command handler."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing trade...")
    
    try:
        # Parse user input
        if not context.args:
            raise ValueError("No trading parameters provided.\nUsage: /trade <buy/sell> <symbol> <amount>\nExample: /trade buy BTC 0.1")

        if len(context.args) != 3:
            raise ValueError("Invalid number of arguments.\nUsage: /trade <buy/sell> <symbol> <amount>\nExample: /trade buy BTC 0.1")

        action, symbol, amount = context.args
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a valid number")

        # Validate input
        if action.lower() not in ['buy', 'sell']:
            raise ValueError("Invalid action. Use 'buy' or 'sell'")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not symbol.isalnum():
            raise ValueError("Invalid symbol format")

        # Check available funds (example with a dummy balance)
        available_balance = 1000  # This should come from your exchange API
        if action.lower() == 'buy' and amount > available_balance:
            raise ValueError(f"Insufficient funds. Available balance: {available_balance}")

        # Execute trade (placeholder for exchange API integration)
        trade_result = {
            'success': True,
            'price': 100,  # Example price
            'amount': amount,
            'total': amount * 100,
            'symbol': symbol.upper()
        }

        if not trade_result['success']:
            raise Exception("Trade execution failed")

        success_message = (
            f"Trade executed successfully!\n"
            f"Action: {action.upper()}\n"
            f"Symbol: {trade_result['symbol']}\n"
            f"Amount: {trade_result['amount']}\n"
            f"Price: ${trade_result['price']}\n"
            f"Total: ${trade_result['total']}"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=success_message)
    except Exception as e:
        error_message = f"❌ Trade failed: {str(e)}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def portfolio(update, context):
    """Portfolio command handler."""
    try:
        # Mock portfolio data - replace with actual data from your database/exchange
        portfolio_data = {
            'BTC': {'amount': 0.5, 'value_usd': 15000},
            'ETH': {'amount': 2.0, 'value_usd': 4000},
            'DOGE': {'amount': 1000, 'value_usd': 100}
        }

        total_value = sum(coin['value_usd'] for coin in portfolio_data.values())

        # Format portfolio message
        portfolio_text = "📊 Your Portfolio:\n\n"
        for symbol, data in portfolio_data.items():
            portfolio_text += f"{symbol}: {data['amount']} (${data['value_usd']:,.2f})\n"
        portfolio_text += f"\n💰 Total Value: ${total_value:,.2f}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=portfolio_text)
    except Exception as e:
        error_message = f"❌ Failed to retrieve portfolio: {str(e)}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def alerts(update, context):
    """Alerts command handler."""
    try:
        if not context.args:
            # Show current alerts
            # Mock data - replace with actual alert data from database
            current_alerts = [
                {"symbol": "BTC", "price": 30000, "condition": "above"},
                {"symbol": "ETH", "price": 2000, "condition": "below"}
            ]
            
            if not current_alerts:
                text = "No active alerts.\n\n"
            else:
                text = "🔔 Your Active Alerts:\n\n"
                for alert in current_alerts:
                    text += f"{alert['symbol']}: {alert['condition']} ${alert['price']:,.2f}\n"
            
            text += "\nUsage:\n/alerts add <symbol> <above/below> <price>\n/alerts remove <symbol>"
            
        elif context.args[0].lower() == "add":
            if len(context.args) != 4:
                raise ValueError("Invalid format. Use: /alerts add <symbol> <above/below> <price>")
            
            _, symbol, condition, price = context.args
            if condition.lower() not in ['above', 'below']:
                raise ValueError("Condition must be 'above' or 'below'")
            
            try:
                price = float(price)
            except ValueError:
                raise ValueError("Price must be a number")
                
            text = f"✅ Alert added for {symbol.upper()} {condition} ${price:,.2f}"
            
        elif context.args[0].lower() == "remove":
            if len(context.args) != 2:
                raise ValueError("Invalid format. Use: /alerts remove <symbol>")
            
            text = f"✅ Alert removed for {context.args[1].upper()}"
            
        else:
            raise ValueError("Invalid command. Use 'add' or 'remove'")
            
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        
    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def status(update, context):
    """Status command handler."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="The bot is running smoothly!")

async def handle_trade_command(update: Update, context: CallbackContext):
    try:
        if len(context.args) != 3:
            raise ValueError("Invalid number of arguments.\nUsage: /trade <buy/sell> <symbol> <amount>\nExample: /trade buy BTC 0.1")

        action, symbol, amount = context.args
        try:
            amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a valid number")

        # Validate input
        if action.lower() not in ['buy', 'sell']:
            raise ValueError("Invalid action. Use 'buy' or 'sell'")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not symbol.isalnum():
            raise ValueError("Invalid symbol format")

        # Check available funds (example with a dummy balance)
        available_balance = 1000  # This should come from your exchange API
        if action.lower() == 'buy' and amount > available_balance:
            await update.message.reply_text(f"Insufficient funds. Available balance: {available_balance}")
            return

        # Execute trade (implement actual trading logic here)
        await update.message.reply_text(f"Trade executed: {action} {amount} {symbol}")

    except ValueError as e:
        await update.message.reply_text(str(e))
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def handle_portfolio_command(update: Update, context: CallbackContext):
    # Implement portfolio command logic
    await update.message.reply_text("Portfolio command not implemented yet")

@bot.command(name='settings')
async def settings(ctx):
    await ctx.send("⚙️ Settings functionality coming soon!")

# Make sure to export the functions
__all__ = ['handle_trade_command', 'handle_portfolio_command']