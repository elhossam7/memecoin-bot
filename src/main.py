import asyncio
import logging
import platform
import signal
from bot.telegram_client import TelegramBot
from utils.config import load_config
import os

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
    bot = TelegramBot(os.getenv('TELEGRAM_BOT_TOKEN'))
    await bot.application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())