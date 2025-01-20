import os
import sys
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.telegram_client import TelegramBot

def main():
    # Load environment variables
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_path):
        print("Error: .env file not found!")
        print("Please create a .env file in the root directory with your BOT_TOKEN")
        sys.exit(1)

    load_dotenv(env_path)
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
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