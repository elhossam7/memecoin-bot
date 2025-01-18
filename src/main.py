import asyncio
import logging
import os
from dotenv import load_dotenv
from bot.telegram_client import TelegramBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the token and verify it exists
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    
    # Initialize the bot    
    bot = TelegramBot(token)
    
    try:
        # Start the bot properly
        await bot.start()
        
        # Keep the bot running
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
    finally:
        # Ensure proper cleanup
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass