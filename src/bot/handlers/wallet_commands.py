import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ...core.wallet.generator import WalletGenerator
from ...core.wallet.storage import WalletStorage
from ...blockchain.solana.web3_client import get_account_balance

# Configure logger
logger = logging.getLogger(__name__)

wallet_storage = WalletStorage()

async def start_wallet_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the wallet creation process."""
    keyboard = [
        [
            InlineKeyboardButton("Ethereum", callback_data='select_eth'),
            InlineKeyboardButton("Solana", callback_data='select_sol')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚀 Let's create your wallet!\n\n"
        "Please select your preferred blockchain network:",
        reply_markup=reply_markup
    )

async def handle_blockchain_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle blockchain selection callback."""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    blockchain = 'ethereum' if query.data == 'select_eth' else 'solana'
    
    try:
        # Check if user already has a wallet
        existing_wallet = wallet_storage.get_wallet(user_id)
        if (existing_wallet):
            await query.edit_message_text(
                "⚠️ You already have a wallet. Use /wallet to view your details."
            )
            return

        # Create confirmation keyboard
        keyboard = [[
            InlineKeyboardButton("✅ Confirm", callback_data=f'create_{blockchain}'),
            InlineKeyboardButton("❌ Cancel", callback_data='cancel_creation')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Show confirmation message
        await query.edit_message_text(
            f"You selected {blockchain.title()} network.\n\n"
            "⚠️ Important:\n"
            "- Your wallet will be created securely\n"
            "- Store backup information safely\n"
            "- Never share private keys\n\n"
            "Would you like to proceed?",
            reply_markup=reply_markup
        )

    except Exception as e:
        await query.edit_message_text(
            f"❌ Error during blockchain selection: {str(e)}\n"
            "Please try again or contact support."
        )

async def handle_wallet_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle wallet creation after confirmation."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'cancel_creation':
        await query.edit_message_text(
            "Wallet creation cancelled. Use /start to try again."
        )
        return
    
    user_id = str(query.from_user.id)
    primary_blockchain = 'ethereum' if query.data == 'create_ethereum' else 'solana'
    
    try:
        # Create wallets for both chains
        wallet_data = WalletGenerator.create_wallet(primary_blockchain)
        
        # Save wallet securely
        if wallet_storage.save_wallet(user_id, wallet_data):
            # Format message with both wallet addresses
            message = (
                f"✅ Wallets created successfully!\n\n"
                f"Primary Network: {primary_blockchain.title()}\n\n"
                f"🔷 Ethereum Wallet:\n`{wallet_data['ethereum']['address']}`\n\n"
                f"🌟 Solana Wallet:\n`{wallet_data['solana']['address']}`\n\n"
                "⚠️ Important: Store your wallet details securely!\n"
                "Use /wallet to view your wallet information."
            )
            
            # Escape special characters for MarkdownV2
            message = message.replace('.', '\\.')
            
            await query.edit_message_text(
                text=message,
                parse_mode='MarkdownV2'
            )
        else:
            raise Exception("Failed to save wallet")

    except Exception as e:
        await query.edit_message_text(
            f"❌ Error creating wallet: {str(e)}\n"
            "Please try again or contact support."
        )

async def create_solana_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a Solana wallet for the user"""
    user_id = update.effective_user.id
    try:
        # Generate wallet using the wallet generator
        wallet_data = WalletGenerator.create_wallet('solana')
        
        if not wallet_data['success']:
            await update.message.reply_text(
                "❌ Failed to create wallet. Please try again later."
            )
            return
            
        # Format the wallet address for display
        address = wallet_data['solana']['address']
        escaped_address = address.replace('-', '\\-').replace('.', '\\.')
        
        # Get initial balance
        balance = await get_account_balance(address)
        
        # Create message with wallet details and funding instructions
        message = (
            "🌟 Your Solana wallet has been created\\!\n\n"
            f"Wallet Address: `{escaped_address}`\n"
            f"Current Balance: {balance} SOL\n\n"
            "⚠️ *Important Instructions*:\n"
            "1\\. Send SOL tokens to this address to start trading\n"
            "2\\. Minimum recommended balance: 0\\.1 SOL\n"
            "3\\. Only send SOL from exchanges or wallets you trust\n\n"
            "Type /balance to check your wallet balance"
        )
        
        await update.message.reply_text(
            message,
            parse_mode='MarkdownV2'
        )

    except Exception as e:
        await update.message.reply_text(
            "❌ Error occurred while creating wallet. Please try again later."
        )
        logger.error(f"Wallet creation error for user {user_id}: {str(e)}")

async def check_wallet_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the user's Solana wallet balance"""
    user_id = update.effective_user.id
    try:
        wallet = wallet_storage.get_wallet(user_id)
        if not wallet:
            await update.message.reply_text(
                "❌ No wallet found. Use /createwallet to create one first."
            )
            return
            
        address = wallet['solana']['address']
        balance = await get_account_balance(address)
        
        if balance < 0.1:
            message = (
                f"Current Balance: {balance} SOL\n\n"
                "⚠️ Your balance is below the recommended 0.1 SOL minimum.\n"
                "Please fund your wallet to start trading."
            )
        else:
            message = (
                f"Current Balance: {balance} SOL\n"
                "✅ Your wallet is funded and ready for trading!"
            )
            
        await update.message.reply_text(message)
        
    except Exception as e:
        await update.message.reply_text(
            "❌ Error checking balance. Please try again later."
        )
        logger.error(f"Balance check error for user {user_id}: {str(e)}")

# Export the handlers
__all__ = ['handle_blockchain_selection', 'handle_wallet_creation', 'create_solana_wallet', 'check_wallet_balance']
