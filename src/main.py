import logging
from bot.telegram_client import TelegramClient
from utils.config import load_config

def main():
    # Load configuration settings
    config = load_config()

    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize the Telegram bot client
    bot = TelegramClient(config['telegram']['token'])

    # Start the bot
    bot.start()
    logger.info("MemeCoin Trading Bot is running...")

if __name__ == "__main__":
    main()