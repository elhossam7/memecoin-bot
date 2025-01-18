import discord
from discord.ext import commands

class TradeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_data = {}  # Initialize settings data storage

    async def setup_hook(self):
        # ...existing code...
        await self.load_extension('bot.settings')
        # ...existing code...

# ...existing code...
