import os
import sys
import logging
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.bot.telegram_client import TelegramBot

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Load environment variables
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        print("Error: BOT_TOKEN not found in .env file!")
        print("Please add BOT_TOKEN=your_telegram_bot_token to your .env file")
        sys.exit(1)
    
    try:
        bot = TelegramBot(token)
        bot.run()
    except Exception as e:
        print(f"Error starting bot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
