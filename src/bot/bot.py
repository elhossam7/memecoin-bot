import discord 
from discord.ext import commands

class TradeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_data = {}  # Initialize settings data storage

    async def setup_hook(self):
        # Load extensions/cogs
        await self.load_extension('bot.settings')
        print('Bot is ready!')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

def run_bot(token):
    # Create bot instance with default intents
    intents = discord.Intents.default()
    intents.message_content = True
    bot = TradeBot(command_prefix='!', intents=intents)
    
    # Run the bot
    bot.run(token)

if __name__ == '__main__':
    # Replace 'YOUR_TOKEN' with your actual bot token
    TOKEN = '7798784053:AAHq4Rh_daQrFqzl9eNg5ZMDcBJQsXNHAfI'
    run_bot(TOKEN)
