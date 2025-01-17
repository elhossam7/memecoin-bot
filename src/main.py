import asyncio
import logging
import platform
import signal
from bot.telegram_client import TelegramClient
from utils.config import load_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def shutdown(bot):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info("Shutting down...")
    await bot.stop()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    bot = None
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        if len(config.telegram_token) < 10:
            logger.error("Telegram token appears to be too short")
            raise ValueError("Invalid token length")
        
        bot = TelegramClient(config.telegram_token)
        
        # Start the bot
        await bot.start()
        logger.info("Bot started successfully")
        
        # Keep the bot running
        while True:
            await asyncio.sleep(1)
            
    except asyncio.CancelledError:
        logger.info("Bot shutdown initiated")
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
    finally:
        if bot:
            await shutdown(bot)
        logger.info("Shutdown complete.")

def handle_exit():
    for task in asyncio.all_tasks():
        task.cancel()

if __name__ == "__main__":
    try:
        if platform.system() == 'Windows':
            # Windows-specific handling
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            # Unix-style signal handling
            asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Process terminated with error: {e}")