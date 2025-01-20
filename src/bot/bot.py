import discord 
from discord.ext import commands
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Event handler for when bot is ready"""
    logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        logger.error(f"Error occurred: {str(error)}")
        await ctx.send("An error occurred while processing your command.")

@bot.command(name='ping')
async def ping(ctx):
    """Simple command to check if bot is responsive"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

def run_bot(token):
    """Run the bot with the provided token"""
    try:
        bot.run(token)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")

if __name__ == "__main__":
    # Replace with your actual token
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    run_bot(TOKEN)
